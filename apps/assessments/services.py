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
        if 50 <= age <= 59:
            return "50-59"
        elif 60 <= age <= 69:
            return "60-69"
        elif 70 <= age <= 79:
            return "70-79"
        else:
            return "80+"
    
    def _get_education_group(self, patient):
        """Determina o grupo educacional baseado no nível de escolaridade"""
        # Prioriza nível; se não houver, usa anos legado
        level = getattr(patient, 'education_level', None)
        years = getattr(patient, 'education_years', None)
        
        if level in ('NONE', 'FUNDAMENTAL', 'MEDIO'):
            return 'low_education'
        if level in ('GRADUACAO', 'POSGRAD'):
            return 'high_education'
        
        if years is not None:
            return 'high_education' if years > 7 else 'low_education'
        
        # Default conservador
        return 'low_education'
    
    def calculate_z_score(self, raw_score, mean, standard_deviation):
        """
        Calcula o Z-Score usando a fórmula: Z = (Escore Bruto - Média) / Desvio Padrão
        Para testes onde maior tempo = pior desempenho (TMT, Stroop): valores positivos indicam déficit
        Para testes onde maior pontuação = melhor desempenho (Digit Span): valores negativos indicam déficit
        """
        if standard_deviation == 0:
            return 0
        return (raw_score - mean) / standard_deviation
    
    def calculate_tmt_z_scores(self, patient, time_a, time_b, errors_a=0, errors_b=0):
        """
        Calcula os Z-Scores para TMT-A e TMT-B
        """
        age_group = self._get_age_group(patient.age)
        education_group = self._get_education_group(patient)
        
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
        education_group = self._get_education_group(patient)
        
        norms = self.normative_data["digit_span"][age_group][education_group]
        return self.calculate_z_score(total_score, norms["mean"], norms["sd"])
    
    def calculate_stroop_z_score(self, patient, interference_time):
        """
        Calcula o Z-Score para Stroop (tempo de interferência)
        """
        age_group = self._get_age_group(patient.age)
        education_group = self._get_education_group(patient)
        
        norms = self.normative_data["stroop"][age_group][education_group]
        return self.calculate_z_score(interference_time, norms["mean"], norms["sd"])
    
    def calculate_meem_z_score(self, patient, total_score):
        """
        Calcula o Z-Score para MEEM (pontuação total 0-30)
        Para MEEM: maior pontuação = melhor desempenho (como Digit Span)
        Valores negativos indicam déficit cognitivo
        """
        age_group = self._get_age_group(patient.age)
        education_group = self._get_education_group(patient)
        
        # Verificar se temos dados normativos para MEEM
        if "meem" in self.normative_data:
            norms = self.normative_data["meem"][age_group][education_group]
            return self.calculate_z_score(total_score, norms["mean"], norms["sd"])
        else:
            # Dados normativos baseados em Brucki et al. (2003) - estimativa
            if education_group == "high_education":
                mean_score = 28.5
                sd_score = 1.8
            else:  # low_education
                mean_score = 25.2
                sd_score = 2.3
            
            return self.calculate_z_score(total_score, mean_score, sd_score)
    
    def calculate_clock_drawing_z_score(self, patient, total_score):
        """
        Calcula Z-Score para o Teste do Relógio (0-10 pontos)
        Baseado em dados normativos de Cacho-Gutiérrez et al. (1999)
        """
        try:
            age = getattr(patient, 'age', 65)
            education_years = getattr(patient, 'education_years', 8)
            
            # Dados normativos aproximados para Clock Drawing Test
            # Pontuação média varia por idade e escolaridade
            if age < 65:
                if education_years <= 8:
                    mean_score = 8.5
                    sd = 1.2
                else:
                    mean_score = 9.2
                    sd = 0.9
            elif age < 75:
                if education_years <= 8:
                    mean_score = 7.8
                    sd = 1.5
                else:
                    mean_score = 8.7
                    sd = 1.1
            else:  # 75+
                if education_years <= 8:
                    mean_score = 7.2
                    sd = 1.8
                else:
                    mean_score = 8.0
                    sd = 1.4
            
            # Calcular Z-Score
            z_score = (total_score - mean_score) / sd
            
            return round(z_score, 2)
            
        except Exception as e:
            print(f"Erro ao calcular Z-Score do Clock Drawing: {e}")
            return 0.0
    
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
            
            # Adicionar MEEM se disponível
            if hasattr(assessment, 'meem_result'):
                meem_result = assessment.meem_result
                total_score = meem_result.total_score
                z_score = self.calculate_meem_z_score(patient, total_score)
                meem_result.z_score = z_score
                meem_result.save()
                z_scores.append(z_score)
            
            # Adicionar Clock Drawing Test se disponível
            if hasattr(assessment, 'clock_drawing_result'):
                clock_result = assessment.clock_drawing_result
                total_score = clock_result.total_score
                z_score = self.calculate_clock_drawing_z_score(patient, total_score)
                clock_result.z_score = z_score
                clock_result.save()
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

def calculate_clock_drawing_z_score(patient, total_score):
    """
    Função específica para calcular Z-Score do Clock Drawing Test
    RF05 - Motor de Pontuação
    """
    return score_calculator.calculate_clock_drawing_z_score(patient, total_score)