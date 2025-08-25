from django import forms
from .models import Assessment, DigitSpanResult, TMTResult, StroopResult, MeemResult, ClockDrawingResult, ClockDrawingResult

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['patient', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class DigitSpanForm(forms.ModelForm):
    class Meta:
        model = DigitSpanResult
        fields = ['forward_score', 'forward_span', 'backward_score', 'backward_span']
        widgets = {
            'forward_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 16}),
            'forward_span': forms.NumberInput(attrs={'class': 'form-control', 'min': 3, 'max': 9}),
            'backward_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 14}),
            'backward_span': forms.NumberInput(attrs={'class': 'form-control', 'min': 2, 'max': 8}),
        }

class TMTForm(forms.ModelForm):
    class Meta:
        model = TMTResult
        fields = ['time_a_seconds', 'errors_a', 'time_b_seconds', 'errors_b']
        widgets = {
            'time_a_seconds': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'errors_a': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'time_b_seconds': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'errors_b': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

class StroopForm(forms.ModelForm):
    class Meta:
        model = StroopResult
        fields = ['card_1_time', 'card_1_errors', 'card_2_time', 'card_2_errors', 'card_3_time', 'card_3_errors']
        widgets = {
            'card_1_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'card_1_errors': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'card_2_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'card_2_errors': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'card_3_time': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'card_3_errors': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class MeemForm(forms.ModelForm):
    """
    Formulário para aplicação do Mini Exame do Estado Mental (MEEM)
    Baseado no protocolo de Folstein & Folstein (1975)
    """
    
    class Meta:
        model = MeemResult
        fields = [
            # Orientação temporal (5 pontos)
            'temporal_weekday', 'temporal_day', 'temporal_month', 'temporal_year', 'temporal_hour',
            # Orientação espacial (5 pontos) 
            'spatial_location', 'spatial_place', 'spatial_neighborhood', 'spatial_city', 'spatial_state',
            # Memória imediata (3 pontos)
            'memory_word1', 'memory_word2', 'memory_word3',
            # Atenção e cálculo (5 pontos)
            'attention_calc1', 'attention_calc2', 'attention_calc3', 'attention_calc4', 'attention_calc5',
            # Evocação (3 pontos)
            'recall_word1', 'recall_word2', 'recall_word3',
            # Nomeação (2 pontos)
            'naming_object1', 'naming_object2',
            # Repetição (1 ponto)
            'repetition_phrase',
            # Comando verbal (3 pontos)
            'command_take', 'command_fold', 'command_put',
            # Comando escrito (1 ponto)
            'written_command',
            # Escrever frase (1 ponto)
            'write_sentence',
            # Copiar desenho (1 ponto)
            'copy_pentagons'
        ]
        
        widgets = {
            # Orientação temporal
            'temporal_weekday': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'temporal_day': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'temporal_month': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'temporal_year': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'temporal_hour': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Orientação espacial
            'spatial_location': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'spatial_place': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'spatial_neighborhood': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'spatial_city': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'spatial_state': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Memória imediata
            'memory_word1': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'memory_word2': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'memory_word3': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Atenção e cálculo
            'attention_calc1': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'attention_calc2': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'attention_calc3': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'attention_calc4': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'attention_calc5': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Evocação
            'recall_word1': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'recall_word2': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'recall_word3': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Nomeação
            'naming_object1': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'naming_object2': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Repetição
            'repetition_phrase': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Comando verbal
            'command_take': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'command_fold': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            'command_put': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Comando escrito
            'written_command': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Escrever frase
            'write_sentence': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
            
            # Copiar desenho
            'copy_pentagons': forms.RadioSelect(choices=[(0, 'Incorreto'), (1, 'Correto')]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Organizar campos por seções para o template
        self.sections = {
            'Orientação Temporal (5 pontos)': {
                'fields': ['temporal_weekday', 'temporal_day', 'temporal_month', 'temporal_year', 'temporal_hour'],
                'instructions': [
                    'Qual o dia da semana?',
                    'Qual a data do mês?',
                    'Em que mês estamos?',
                    'Em que ano estamos?',
                    'Que horas são agora? (tolerância de 60 minutos)'
                ]
            },
            'Orientação Espacial (5 pontos)': {
                'fields': ['spatial_location', 'spatial_place', 'spatial_neighborhood', 'spatial_city', 'spatial_state'],
                'instructions': [
                    'Que local é este? (consultório, quarto, etc.)',
                    'Onde fica o local em que estamos? (hospital, clínica, casa)',
                    'Qual o bairro ou nome de rua próxima?',
                    'Qual a cidade?',
                    'Qual o estado?'
                ]
            },
            'Memória Imediata (3 pontos)': {
                'fields': ['memory_word1', 'memory_word2', 'memory_word3'],
                'instructions': [
                    'Primeira palavra: CARRO',
                    'Segunda palavra: VASO', 
                    'Terceira palavra: TIJOLO'
                ],
                'instruction_text': 'Diga ao paciente: "Vou dizer três palavras e gostaria que você as decorasse pois vou perguntá-las novamente depois"'
            },
            'Atenção e Cálculo (5 pontos)': {
                'fields': ['attention_calc1', 'attention_calc2', 'attention_calc3', 'attention_calc4', 'attention_calc5'],
                'instructions': [
                    '100 - 7 = 93',
                    '93 - 7 = 86',
                    '86 - 7 = 79',
                    '79 - 7 = 72',
                    '72 - 7 = 65'
                ],
                'instruction_text': 'Peça para o paciente realizar subtrações seriadas de 7 a partir de 100'
            },
            'Memória de Evocação (3 pontos)': {
                'fields': ['recall_word1', 'recall_word2', 'recall_word3'],
                'instructions': [
                    'Evocação: CARRO',
                    'Evocação: VASO',
                    'Evocação: TIJOLO'
                ],
                'instruction_text': 'Peça para o paciente repetir as três palavras ditas anteriormente (sem dar pistas)'
            },
            'Nomeação (2 pontos)': {
                'fields': ['naming_object1', 'naming_object2'],
                'instructions': [
                    'Mostrar relógio e pedir para nomear',
                    'Mostrar caneta e pedir para nomear'
                ]
            },
            'Repetição (1 ponto)': {
                'fields': ['repetition_phrase'],
                'instructions': ['Repetir: "Nem aqui, nem ali, nem lá"'],
                'instruction_text': 'Considerar apenas a primeira tentativa (pode repetir a frase se não entendeu)'
            },
            'Comando Verbal (3 pontos)': {
                'fields': ['command_take', 'command_fold', 'command_put'],
                'instructions': [
                    'Pegar a folha com a mão direita',
                    'Dobrar ao meio',
                    'Colocar no chão'
                ],
                'instruction_text': 'Entregue uma folha de papel e diga: "Pegue a folha com a mão direita, dobre-a ao meio e coloque no chão"'
            },
            'Comando Escrito (1 ponto)': {
                'fields': ['written_command'],
                'instructions': ['Ler e executar: "FECHE OS OLHOS"'],
                'instruction_text': 'Mostre uma folha com o comando escrito claramente'
            },
            'Escrever Frase (1 ponto)': {
                'fields': ['write_sentence'],
                'instructions': ['Frase com verbo e sentido completo'],
                'instruction_text': 'Peça para escrever uma frase com início, meio e fim (deve conter um verbo)'
            },
            'Copiar Desenho (1 ponto)': {
                'fields': ['copy_pentagons'],
                'instructions': ['Copiar dois pentágonos intersectados'],
                'instruction_text': 'Apresente o desenho dos pentágonos intersectados para cópia'
            }
        }
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-check-input'})
    
    def get_total_possible_score(self):
        """Retorna a pontuação total possível (30 pontos)"""
        return 30
    
    def get_sections_with_fields(self):
        """Retorna as seções organizadas com os campos do formulário"""
        sections_with_fields = {}
        for section_name, section_data in self.sections.items():
            sections_with_fields[section_name] = {
                **section_data,
                'form_fields': [self[field_name] for field_name in section_data['fields']]
            }
        return sections_with_fields

class ClockDrawingForm(forms.ModelForm):
    """Formulário para o Teste do Relógio"""
    
    class Meta:
        model = ClockDrawingResult
        fields = [
            'requested_time',
            'circle_score', 
            'numbers_score', 
            'hands_score',
            'observations',
            'drawing_data'
        ]
        
        widgets = {
            'requested_time': forms.Select(
                attrs={'class': 'form-control'},
                choices=[
                    ('10:05', '10:05'),
                    ('11:10', '11:10'),
                    ('14:30', '14:30'),
                    ('15:45', '15:45'),
                    ('20:20', '20:20')
                ]
            ),
            'circle_score': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'numbers_score': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'hands_score': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'observations': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Descreva o processo de execução, dificuldades observadas, comportamentos durante o teste...'
            }),
            'drawing_data': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Definir labels mais descritivos
        self.fields['requested_time'].label = "Hora Solicitada"
        self.fields['circle_score'].label = "Círculo (0-2 pontos)"
        self.fields['numbers_score'].label = "Números (0-4 pontos)"  
        self.fields['hands_score'].label = "Ponteiros (0-4 pontos)"
        self.fields['observations'].label = "Observações"
        
        # Adicionar help_text
        self.fields['circle_score'].help_text = "Avalie a qualidade do círculo desenhado"
        self.fields['numbers_score'].help_text = "Avalie se todos os 12 números estão presentes e bem posicionados"
        self.fields['hands_score'].help_text = "Avalie se os ponteiros indicam corretamente a hora solicitada"
        
        # Definir valor padrão para requested_time
        if not self.instance.pk:
            self.fields['requested_time'].initial = '10:05'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que todos os componentes foram pontuados
        circle_score = cleaned_data.get('circle_score')
        numbers_score = cleaned_data.get('numbers_score')
        hands_score = cleaned_data.get('hands_score')
        
        if circle_score is None or numbers_score is None or hands_score is None:
            raise forms.ValidationError(
                "Todos os componentes devem ser pontuados: círculo, números e ponteiros."
            )
        
        return cleaned_data
    
    def get_score_breakdown(self):
        """Retorna detalhamento da pontuação"""
        if not self.instance.pk:
            return None
            
        return {
            'circle': {
                'score': self.instance.circle_score,
                'max': 2,
                'percentage': (self.instance.circle_score / 2) * 100
            },
            'numbers': {
                'score': self.instance.numbers_score,
                'max': 4,
                'percentage': (self.instance.numbers_score / 4) * 100
            },
            'hands': {
                'score': self.instance.hands_score,
                'max': 4, 
                'percentage': (self.instance.hands_score / 4) * 100
            },
            'total': {
                'score': self.instance.total_score,
                'max': 10,
                'percentage': (self.instance.total_score / 10) * 100
            }
        }
