/**
 * Sistema de Cores e Utilitários para Z-Scores
 * Baseado no novo sistema de classificação implementado
 */

// Função para obter cor baseada no Z-score
function getZScoreColor(zScore) {
    if (zScore <= -2.5) return '#6f42c1'; // CRITICAL - Roxo
    if (zScore <= -1.5) return '#dc3545'; // HIGH - Vermelho  
    if (zScore <= -1.0) return '#fd7e14'; // MODERATE - Laranja
    if (zScore <= -0.5) return '#ffc107'; // LOW - Amarelo
    return '#28a745'; // MINIMAL - Verde
}

// Função para obter rótulo baseado no Z-score
function getZScoreLabel(zScore) {
    if (zScore <= -2.5) return 'Crítico';
    if (zScore <= -1.5) return 'Alto';  
    if (zScore <= -1.0) return 'Moderado';
    if (zScore <= -0.5) return 'Baixo';
    return 'Mínimo';
}

// Função para obter percentil do Z-score
function getZScorePercentile(zScore) {
    // Aproximação da função CDF da distribuição normal
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p = 0.3275911;
    
    const sign = zScore >= 0 ? 1 : -1;
    const x = Math.abs(zScore) / Math.sqrt(2.0);
    
    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    
    return Math.round((0.5 * (1.0 + sign * y)) * 100 * 100) / 100;
}

// Configurações padrão para gráficos de Z-score
const zScoreChartDefaults = {
    scales: {
        y: {
            beginAtZero: false,
            min: -3,
            max: 3,
            ticks: {
                stepSize: 0.5,
                callback: function(value) {
                    return value.toFixed(1);
                }
            },
            grid: {
                color: function(context) {
                    // Linha mais forte no zero
                    if (Math.abs(context.tick.value) < 0.1) {
                        return '#000000';
                    }
                    // Linhas críticas em -2.5, -1.5, -1.0, -0.5
                    if ([-2.5, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.5].includes(context.tick.value)) {
                        return '#ff6b6b';
                    }
                    return 'rgba(0,0,0,0.1)';
                },
                lineWidth: function(context) {
                    if (Math.abs(context.tick.value) < 0.1) return 2;
                    if ([-2.5, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.5].includes(context.tick.value)) return 1.5;
                    return 1;
                }
            },
            title: {
                display: true,
                text: 'Z-Score'
            }
        }
    },
    plugins: {
        tooltip: {
            callbacks: {
                afterLabel: function(context) {
                    const zScore = context.parsed.y;
                    const label = getZScoreLabel(zScore);
                    const percentile = getZScorePercentile(zScore);
                    return [
                        `Classificação: ${label}`,
                        `Percentil: ${percentile}%`
                    ];
                }
            }
        }
    }
};

// Função para aplicar cores dinâmicas aos elementos da interface
function applyZScoreColors() {
    // Aplicar cores aos elementos com classe z-score-value
    document.querySelectorAll('.z-score-value').forEach(element => {
        const score = parseFloat(element.dataset.score || element.textContent);
        if (!isNaN(score)) {
            const color = getZScoreColor(score);
            element.style.color = color;
            element.style.fontWeight = 'bold';
            
            // Adicionar tooltip com informações
            element.title = `Z-Score: ${score.toFixed(2)} | ${getZScoreLabel(score)} | Percentil: ${getZScorePercentile(score)}%`;
        }
    });
    
    // Aplicar cores aos cards de estatísticas
    document.querySelectorAll('.test-stat-card').forEach(card => {
        const scoreElement = card.querySelector('[data-avg-score]');
        if (scoreElement) {
            const avgScore = parseFloat(scoreElement.dataset.avgScore);
            if (!isNaN(avgScore)) {
                const color = getZScoreColor(avgScore);
                card.style.borderLeft = `4px solid ${color}`;
                scoreElement.style.color = color;
            }
        }
    });
}

// Configuração específica para gráficos de testes de tempo
const timeTestChartDefaults = {
    scales: {
        y: {
            beginAtZero: false,
            reverse: false, // Não inverter, valores menores são melhores mas mostrar normalmente
            title: {
                display: true,
                text: 'Z-Score Normalizado'
            },
            ticks: {
                callback: function(value) {
                    return value.toFixed(1);
                }
            }
        }
    },
    plugins: {
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.parsed.y;
                    return `${context.dataset.label}: ${value.toFixed(2)} (melhor desempenho = valores mais negativos)`;
                }
            }
        }
    }
};

// Configuração específica para gráficos de testes de performance  
const performanceTestChartDefaults = {
    scales: {
        y: {
            beginAtZero: false,
            title: {
                display: true,
                text: 'Z-Score'
            },
            ticks: {
                callback: function(value) {
                    return value.toFixed(1);
                }
            }
        }
    },
    plugins: {
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.parsed.y;
                    return `${context.dataset.label}: ${value.toFixed(2)} (melhor desempenho = valores mais positivos)`;
                }
            }
        }
    }
};

// Executar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    applyZScoreColors();
});

// Exportar para uso global
window.ZScoreUtils = {
    getColor: getZScoreColor,
    getLabel: getZScoreLabel,
    getPercentile: getZScorePercentile,
    chartDefaults: zScoreChartDefaults,
    timeTestDefaults: timeTestChartDefaults,
    performanceTestDefaults: performanceTestChartDefaults,
    applyColors: applyZScoreColors
};
