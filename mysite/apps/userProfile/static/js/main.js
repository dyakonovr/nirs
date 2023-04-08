$(document).ready(() => {
    csrf()
    changePasswordForm()
})

function csrf() {
    function getCookie(name) {
        var cookieValue = null;

        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        const host = document.location.host;
        const protocol = document.location.protocol;
        const sr_origin = "//" + host;
        const origin = protocol + sr_origin;

        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader('X-CSRFtoken', $('input[name="csrfmiddlewaretoken"]').val());
            }
        }
    })
}

function changePasswordForm() {
    const formId = 'form#change_password';
    const formBut = '#form-button'

    $(formId).on('submit', (e) => {
        e.preventDefault();
        $.ajax({
            url: 'profile',
            type: 'POST',
            dataType: 'json',
            data: {
                oldPassword: $(formId + ' #id_oldPassword').val(),
                newPassword: $(formId + ' #id_newPassword').val(),
                passwordConfirm: $(formId + ' #id_passwordConfirm').val(),
            },
            success: function (data) {
                if ('errors' in data) {
                    $(formId + ' .invalid-feedback').each((index, el) => {
                        $(el).remove();
                    });
                    $(formId + ' .is-invalid').each((index, e2) => {
                        $(e2).removeClass('is-invalid');
                    });
                    $(formId).find('.text-success').remove();

                    for (let key in data['errors']) {
                        let result = '';
                        if (key == '__all__') {
                            $(formId).find('input#id_newPassword').addClass('is-invalid');
                            $(formId).find('input#id_passwordConfirm').addClass('is-invalid');

                            $(formId).find('#id_passwordConfirm').after(() => {
                                for (let k in data['errors'][key]) {
                                    result += data['errors'][key][k] + '<br>';
                                }
                                return '<div class="invalid-feedback">' + result + '</div>'
                            })

                        }
                        else {
                            $(formId).find('input[name="' + key + '"]').addClass('is-invalid');
                            console.log($(formId).find('input[name="' + key + '"]'))
                            $(formId).find('input[name="' + key + '"]').after(() => {


                                for (let k in data['errors'][key]) {
                                    result += data['errors'][key][k] + '<br>';
                                }

                                return '<div class="invalid-feedback">' + result + '</div>'
                            });

                        }

                    }
                }

                if ('success' in data) {
                    $(formId + ' .invalid-feedback').each((index, el) => {
                        $(el).remove();
                    });
                    $(formId + ' .is-invalid').each((index, e2) => {
                        $(e2).removeClass('is-invalid');
                    });
                    $(formId).find('.text-success').remove();
                    $(formId + ' input').each((index, e2) => {
                        $(e2).addClass('is-valid');
                    });

                    $(formId).find(formBut).after(() => {
                        return '<span class="text-success">' + data['success'] + '</span>'
                    })
                }
            },
            error: function (data) {
                console.log('Server Error')
            }
        })
    });
}