"""
Utilitários para normalização consistente de Z-scores no sistema CareSense.

Este módulo fornece funções para garantir que todos os Z-scores sejam interpretados
de forma consistente em todo o sistema, onde valores negativos sempre indicam déficit.
"""

def normalize_z_score_for_deficit(z_score, test_type):
    """
    Normaliza Z-scores para que valores negativos sempre indiquem déficit.
    
    Args:
        z_score (float): Z-score bruto calculado
        test_type (str): Tipo do teste
            - 'performance': maior pontuação = melhor (Digit Span, MEEM, Clock Drawing)
            - 'time': menor tempo = melhor (TMT, Stroop)
    
    Returns:
        float: Z-score normalizado onde valores negativos = déficit
        
    Examples:
        >>> normalize_z_score_for_deficit(-1.5, 'performance')  # Digit Span baixo
        -1.5
        
        >>> normalize_z_score_for_deficit(2.0, 'time')  # TMT muito lento
        -2.0
        
        >>> normalize_z_score_for_deficit(-0.5, 'time')  # TMT rápido
        -0.5
    """
    if test_type == 'performance':
        # Para testes de performance: Z-score já está correto
        # Valores negativos = performance abaixo da média = déficit
        return z_score
    elif test_type == 'time':
        # Para testes de tempo: normalizar para que positivo = déficit
        # Z-score positivo = tempo maior que média = pior performance = déficit (negativo)
        return -abs(z_score) if z_score > 0 else z_score
    else:
        raise ValueError(f"Tipo de teste inválido: {test_type}. Use 'performance' ou 'time'.")

def get_test_type(test_name):
    """
    Retorna o tipo de teste para normalização correta.
    
    Args:
        test_name (str): Nome do teste
        
    Returns:
        str: 'performance' ou 'time'
        
    Raises:
        ValueError: Se o teste não for reconhecido
    """
    performance_tests = ['digit_span', 'meem', 'clock_drawing']
    time_tests = ['tmt_a', 'tmt_b', 'stroop']
    
    if test_name in performance_tests:
        return 'performance'
    elif test_name in time_tests:
        return 'time'
    else:
        raise ValueError(f"Teste não reconhecido: {test_name}")

def normalize_assessment_z_scores(assessment):
    """
    Normaliza todos os Z-scores de uma avaliação para déficit.
    
    Args:
        assessment: Objeto Assessment com resultados de testes
        
    Returns:
        dict: Z-scores normalizados por teste
    """
    normalized_scores = {}
    
    # Digit Span - Performance test
    if hasattr(assessment, 'digit_span_result') and assessment.digit_span_result.z_score is not None:
        normalized_scores['digit_span'] = normalize_z_score_for_deficit(
            assessment.digit_span_result.z_score, 'performance'
        )
    
    # TMT - Time tests
    if hasattr(assessment, 'tmt_result'):
        if assessment.tmt_result.z_score_a is not None:
            normalized_scores['tmt_a'] = normalize_z_score_for_deficit(
                assessment.tmt_result.z_score_a, 'time'
            )
        if assessment.tmt_result.z_score_b is not None:
            normalized_scores['tmt_b'] = normalize_z_score_for_deficit(
                assessment.tmt_result.z_score_b, 'time'
            )
    
    # Stroop - Time test
    if hasattr(assessment, 'stroop_result') and assessment.stroop_result.z_score is not None:
        normalized_scores['stroop'] = normalize_z_score_for_deficit(
            assessment.stroop_result.z_score, 'time'
        )
    
    # MEEM - Performance test
    if hasattr(assessment, 'meem_result') and assessment.meem_result.z_score is not None:
        normalized_scores['meem'] = normalize_z_score_for_deficit(
            assessment.meem_result.z_score, 'performance'
        )
    
    # Clock Drawing - Performance test
    if hasattr(assessment, 'clock_drawing_result') and assessment.clock_drawing_result.z_score is not None:
        normalized_scores['clock_drawing'] = normalize_z_score_for_deficit(
            assessment.clock_drawing_result.z_score, 'performance'
        )
    
    return normalized_scores

def calculate_composite_z_score(normalized_scores):
    """
    Calcula Z-score composto simples (média) dos testes normalizados.
    
    Args:
        normalized_scores (dict): Z-scores normalizados
        
    Returns:
        float: Z-score composto médio
    """
    if not normalized_scores:
        return 0.0
    
    scores = list(normalized_scores.values())
    return sum(scores) / len(scores)

def interpret_z_score(z_score):
    """
    Interpreta um Z-score normalizado em categorias clínicas.
    
    Args:
        z_score (float): Z-score normalizado (negativo = déficit)
        
    Returns:
        tuple: (categoria, descrição, cor)
    """
    if z_score >= -0.5:
        return ('normal', 'Normal', '#28a745')
    elif z_score >= -1.0:
        return ('borderline', 'Limítrofe', '#ffc107')
    elif z_score >= -1.5:
        return ('mild', 'Déficit Leve', '#fd7e14')
    elif z_score >= -2.0:
        return ('moderate', 'Déficit Moderado', '#dc3545')
    else:
        return ('severe', 'Déficit Severo', '#6f42c1')

def get_percentile_from_z_score(z_score):
    """
    Converte Z-score em percentil aproximado.
    
    Args:
        z_score (float): Z-score normalizado
        
    Returns:
        int: Percentil aproximado (0-100)
    """
    # Aproximação simples baseada na distribuição normal
    import math
    
    def normal_cdf(x):
        # Aproximação da função de distribuição cumulativa normal
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    percentile = normal_cdf(z_score) * 100
    return max(0, min(100, round(percentile)))
