{% load i18n %}
var config = {
    eth: {
        fiatExchangeRate: {{ eth.fiatExchangeRate }}
    },
    token: {
        price: {{ token.price }},
        bonus: {{ token.bonus }},
        minTokenAmount:0,
        maxTokenAmount:{{ token.cap }}
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
