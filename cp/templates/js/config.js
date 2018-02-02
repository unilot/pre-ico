{% load i18n %}
var config = {
    eth: {
        fiatExchangeRate: {{ eth.fiatExchangeRate }}
    },
    token: {
        price: {{ token.price }},
        bonus: {{ token.bonus }},
        minTokenAmount:1,
        maxTokenAmount: {{token.available}},
        saleProgress: {{token.sale_progress}},
        saleAmount: {{token.sale_amount}}
    },
    messages: {
        errors: {
            validation: {
                invalidWallet: '{% trans 'Invalid wallet' %}',
                invalidPhone: '{% trans 'Phone number is invalid' %}',
                requestFailed: '{% trans 'Validation failed (Request failed)' %}'
            }
        }
    }
};
