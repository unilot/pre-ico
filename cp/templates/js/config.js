{% load i18n %}
var config = {
    eth: {
        fiatExchangeRate: {{ eth.fiatExchangeRate }}
    },
    token: {
        price: {{ token.price }},
        bonus: {{ token.bonus }},
        minTokenAmount:1,
        maxTokenAmount:0,
        saleProgress: {{sale_progress}},
        saleAmount: {{sale_amount}}
    },
    messages: {
        errors: {
            validation: {
                invalidWallet: '{% trans 'Invalid wallet' %}',
                invalidPhone: '{% trans 'Phone is invalid' %}',
                requestFailed: '{% trans 'Validation failed (Request failed)' %}'
            }
        }
    }
};
