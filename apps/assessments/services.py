import json
import os
from django.conf import settings
from django.utils import timezone
from .models import Assessment, DigitSpanResult, TMTResult, StroopResult

class AssessmentScoreCalculator:
    """
    Classe responsável por calcular os Z-Scores e a pontuação final de risco
    """
    
    def __init__(self):
        self.normative_data = self._load_normative_data()
    
    def _load_normative_data(self):
        """
        Carrega os dados normativos dos testes do arquivo JSON
        """
        try:
            import json
            from pathlib import Path
            
            # Caminho para o arquivo de dados normativos
            data_path = Path(__file__).parent / 'normative_data.json'
            
            with open(data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Fallback para dados exemplo se o arquivo não existir
            print(f"Aviso: Não foi possível carregar dados normativos do arquivo. Usando dados exemplo. Erro: {e}")
            return self._get_example_normative_data()
    
    def _get_example_normative_data(self):
        """
        Dados normativos exemplo - usar apenas como fallback
        """
        return {
            "tmt_a": {
                "60-69": {
                    "low_education": {"mean": 38.5, "sd": 15.2}, 
                    "high_education": {"mean": 29.8, "sd": 10.1}
                },
                "70-79": {
                    "low_education": {"mean": 55.1, "sd": 21.3}, 
                    "high_education": {"mean": 40.2, "sd": 14.7}
                },
                "80+": {
                    "low_education": {"mean": 70.8, "sd": 28.9}, 
                    "high_education": {"mean": 58.4, "sd": 22.1}
                }
            },
            "tmt_b": {
                "60-69": {
                    "low_education": {"mean": 95.2, "sd": 35.4}, 
                    "high_education": {"mean": 70.1, "sd": 25.8}
                },
                "70-79": {
                    "low_education": {"mean": 135.7, "sd": 48.2}, 
                    "high_education": {"mean": 98.3, "sd": 32.1}
                },
                "80+": {
                    "low_education": {"mean": 180.5, "sd": 65.7}, 
                    "high_education": {"mean": 140.2, "sd": 45.3}
                }
            },
            "digit_span": {
                "60-69": {
                    "low_education": {"mean": 10.8, "sd": 2.1}, 
                    "high_education": {"mean": 12.4, "sd": 2.3}
                },
                "70-79": {
                    "low_education": {"mean": 9.5, "sd": 2.4}, 
                    "high_education": {"mean": 11.2, "sd": 2.6}
                },
                "80+": {
                    "low_education": {"mean": 8.1, "sd": 2.8}, 
                    "high_education": {"mean": 9.8, "sd": 2.9}
                }
            },
            "stroop": {
                "60-69": {
                    "low_education": {"mean": 45.2, "sd": 12.3}, 
                    "high_education": {"mean": 35.8, "sd": 9.1}
                },
                "70-79": {
                    "low_education": {"mean": 58.7, "sd": 16.8}, 
                    "high_education": {"mean": 44.2, "sd": 12.4}
                },
                "80+": {
                    "low_education": {"mean": 75.3, "sd": 22.1}, 
                    "high_education": {"mean": 58.9, "sd": 16.7}
                }
            }
        }
    
    def _get_age_group(self, age):
        """Determina o grupo etário baseado na idade"""
        if 60 <= age <= 69:
            return "60-69"
        elif 70 <= age <= 79:
            return "70-79"
        else:
            return "80+"
    
    def _get_education_group(self, education_years):
        """Determina o grupo educacional baseado nos anos de estudo"""
        return "high_education" if education_years >= 8 else "low_education"
    
    def calculate_z_score(self, raw_score, mean, standard_deviation):
        """
        Calcula o Z-Score usando a fórmula: Z = (Média - Escore Bruto) / Desvio Padrão
        """
        if standard_deviation == 0:
            return 0
        return (mean - raw_score) / standard_deviation
    
    def calculate_tmt_z_scores(self, patient, time_a, time_b, errors_a=0, errors_b=0):
        """
        Calcula os Z-Scores para TMT-A e TMT-B
        """
        age_group = self._get_age_group(patient.age)
        education_group = self._get_education_group(patient.education_level)
        
        # Dados normativos para TMT-A
        tmt_a_norms = self.normative_data["tmt_a"][age_group][education_group]
        z_score_a = self.calculate_z_score(time_a, tmt_a_norms["mean"], tmt_a_norms["sd"])
        
        # Dados normativos para TMT-B
        tmt_b_norms = self.normative_data["tmt_b"][age_group][education_group]
        z_score_b = self.calculate_z_score(time_b, tmt_b_norms["mean"], tmt_b_norms["sd"])
        
        return z_score_a, z_score_b
    
    def calculate_digit_span_z_score(self, patient, total_score):
        """
        Calcula o Z-Score para Digit Span (soma de forward + backward)
        """
        age_group = self._get_age_group(patient.age)
        education_group = self._get_education_group(patient.education_level)
        
        norms = self.normative_data["digit_span"][age_group][education_group]
        return self.calculate_z_score(total_score, norms["mean"], norms["sd"])
    
    def calculate_stroop_z_score(self, patient, interference_time):
        """
        Calcula o Z-Score para Stroop (tempo de interferência)
        """
        age_group = self._get_age_group(patient.age)
        education_group = self._get_education_group(patient.education_level)
        
        norms = self.normative_data["stroop"][age_group][education_group]
        return self.calculate_z_score(interference_time, norms["mean"], norms["sd"])
    
    def calculate_final_risk_score(self, assessment_id):
        """
        Calcula a pontuação final de risco baseada nos Z-Scores dos três testes
        """
        try:
            assessment = Assessment.objects.get(id=assessment_id)
            patient = assessment.patient
            
            z_scores = []
            
            # Coleta Z-Scores dos testes completados
            if hasattr(assessment, 'digit_span_result'):
                digit_result = assessment.digit_span_result
                total_score = digit_result.total_score
                z_score = self.calculate_digit_span_z_score(patient, total_score)
                digit_result.z_score = z_score
                digit_result.save()
                z_scores.append(z_score)
            
            if hasattr(assessment, 'tmt_result'):
                tmt_result = assessment.tmt_result
                z_score_a, z_score_b = self.calculate_tmt_z_scores(
                    patient, 
                    tmt_result.time_a_seconds, 
                    tmt_result.time_b_seconds,
                    tmt_result.errors_a,
                    tmt_result.errors_b
                )
                tmt_result.z_score_a = z_score_a
                tmt_result.z_score_b = z_score_b
                tmt_result.save()
                z_scores.extend([z_score_a, z_score_b])
            
            if hasattr(assessment, 'stroop_result'):
                stroop_result = assessment.stroop_result
                # Calcula tempo de interferência (Card 3 é o de interferência)
                interference_time = stroop_result.interference_time
                z_score = self.calculate_stroop_z_score(patient, interference_time)
                stroop_result.z_score = z_score
                stroop_result.save()
                z_scores.append(z_score)
            
            # Determina o risco final baseado na média dos Z-Scores
            if z_scores:
                avg_z_score = sum(z_scores) / len(z_scores)
                
                if avg_z_score <= -2.0:
                    risk_score = 'CRITICAL'
                elif avg_z_score <= -1.5:
                    risk_score = 'HIGH'
                elif avg_z_score <= -1.0:
                    risk_score = 'MODERATE'
                else:
                    risk_score = 'LOW'
                
                assessment.final_risk_score = risk_score
                assessment.mark_completed()
                
                return risk_score
            
            return None
            
        except Assessment.DoesNotExist:
            raise ValueError(f"Assessment with id {assessment_id} not found")

# Instância global do calculador
score_calculator = AssessmentScoreCalculator()

def calculate_final_risk(assessment_id):
    """
    Função de conveniência para calcular o risco final
    RF05 - Motor de Pontuação
    """
    return score_calculator.calculate_final_risk_score(assessment_id)

def calculate_tmt_z_score(patient, time_seconds, errors):
    """
    Função específica para calcular Z-Score do TMT
    RF05 - Motor de Pontuação
    """
    return score_calculator.calculate_tmt_z_scores(patient, time_seconds, 0, errors, 0)