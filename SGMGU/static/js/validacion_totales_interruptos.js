/**
 * Created by ddiaz on 25/01/2019.
 */

/**
 * Created by Daniel.
 */

$(document).on('ready', function () {

    $('#registrar_interrupto').bootstrapValidator({
       // live: 'disabled',
       //  message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            //  Reubicados temporal (dentro de la entidad):
            hastatreintadias_reubicadostemporal_misma_entidad: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            entretreintaysesentadias_reubicadostemporal_misma_entidad: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdesesentayunanno_reubicadostemporal_misma_entidad: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdeunanno_reubicadostemporal_misma_entidad: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            //  Reubicados temporal (fuera de la entidad y dentro del organismo):
            hastatreintadias_reubicadostemporal_mismo_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            entretreintaysesentadias_reubicadostemporal_mismo_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdesesentayunanno_reubicadostemporal_mismo_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdeunanno_reubicadostemporal_mismo_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            //    Reubicados temporal (otro organismo):
            hastatreintadias_reubicadostemporal_otro_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            entretreintaysesentadias_reubicadostemporal_otro_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdesesentayunanno_reubicadostemporal_otro_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdeunanno_reubicadostemporal_otro_organismo: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            //    Cobrando garantía salarial:
            hastatreintadias_cobrandogarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            entretreintaysesentadias_cobrandogarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdesesentayunanno_cobrandogarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdeunanno_cobrandogarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            //    Sin garantía salarial:
            hastatreintadias_singarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            entretreintaysesentadias_singarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdesesentayunanno_singarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdeunanno_singarantiasalarial: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            //  Baja por no aceptar reubicación:
            hastatreintadias_baja: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            entretreintaysesentadias_baja: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdesesentayunanno_baja: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdeunanno_baja: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            //    Propuesto a disponibles:
            hastatreintadias_propuestoadisponibles: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            entretreintaysesentadias_propuestoadisponibles: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdesesentayunanno_propuestoadisponibles: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt(value) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt($('#id_masdeunanno_propuestoadisponibles').val());

                            return total == suma;
                        }
                    }
                }
            },
            masdeunanno_propuestoadisponibles: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt($('#id_hastatreintadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_hastatreintadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_singarantiasalarial').val()) +
                                    parseInt($('#id_hastatreintadias_baja').val()) +
                                    parseInt($('#id_hastatreintadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_entretreintaysesentadias_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_singarantiasalarial').val()) +
                                    parseInt($('#id_entretreintaysesentadias_baja').val()) +
                                    parseInt($('#id_entretreintaysesentadias_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdesesentayunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdesesentayunanno_baja').val()) +
                                    parseInt($('#id_masdesesentayunanno_propuestoadisponibles').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_misma_entidad').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_mismo_organismo').val()) +
                                    parseInt($('#id_masdeunanno_reubicadostemporal_otro_organismo').val()) +
                                    parseInt($('#id_masdeunanno_cobrandogarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_singarantiasalarial').val()) +
                                    parseInt($('#id_masdeunanno_baja').val()) +
                                    parseInt(value);

                            return total == suma;
                        }
                    }
                }
            },
            causa_interrupcion_rotura: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                       parseInt($('#id_causa_interrupcion_falta_piezas').val()) +
                                       parseInt($('#id_causa_interrupcion_accion_lluvia').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_energia').val()) +
                                       parseInt($('#id_causa_interrupcion_orden_paralizacion_temporal').val()) +
                                       parseInt($('#id_causa_interrupcion_paralizacion_reparacion').val()) +
                                       parseInt($('#id_causa_interrupcion_otras_causas').val());

                            return total == suma;
                        }
                    }
                }
            },
            causa_interrupcion_falta_piezas: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                       parseInt($('#id_causa_interrupcion_rotura').val()) +
                                       parseInt($('#id_causa_interrupcion_accion_lluvia').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_energia').val()) +
                                       parseInt($('#id_causa_interrupcion_orden_paralizacion_temporal').val()) +
                                       parseInt($('#id_causa_interrupcion_paralizacion_reparacion').val()) +
                                       parseInt($('#id_causa_interrupcion_otras_causas').val());

                            return total == suma;
                        }
                    }
                }
            },
            causa_interrupcion_accion_lluvia: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                       parseInt($('#id_causa_interrupcion_rotura').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_piezas').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_energia').val()) +
                                       parseInt($('#id_causa_interrupcion_orden_paralizacion_temporal').val()) +
                                       parseInt($('#id_causa_interrupcion_paralizacion_reparacion').val()) +
                                       parseInt($('#id_causa_interrupcion_otras_causas').val());

                            return total == suma;
                        }
                    }
                }
            },
            causa_interrupcion_falta_energia: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                       parseInt($('#id_causa_interrupcion_rotura').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_piezas').val()) +
                                       parseInt($('#id_causa_interrupcion_accion_lluvia').val()) +
                                       parseInt($('#id_causa_interrupcion_orden_paralizacion_temporal').val()) +
                                       parseInt($('#id_causa_interrupcion_paralizacion_reparacion').val()) +
                                       parseInt($('#id_causa_interrupcion_otras_causas').val());

                            return total == suma;
                        }
                    }
                }
            },
            causa_interrupcion_orden_paralizacion_temporal: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                       parseInt($('#id_causa_interrupcion_rotura').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_piezas').val()) +
                                       parseInt($('#id_causa_interrupcion_accion_lluvia').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_energia').val()) +
                                       parseInt($('#id_causa_interrupcion_paralizacion_reparacion').val()) +
                                       parseInt($('#id_causa_interrupcion_otras_causas').val());

                            return total == suma;
                        }
                    }
                }
            },
            causa_interrupcion_paralizacion_reparacion: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                       parseInt($('#id_causa_interrupcion_rotura').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_piezas').val()) +
                                       parseInt($('#id_causa_interrupcion_accion_lluvia').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_energia').val()) +
                                       parseInt($('#id_causa_interrupcion_orden_paralizacion_temporal').val()) +
                                       parseInt($('#id_causa_interrupcion_otras_causas').val());

                            return total == suma;
                        }
                    }
                }
            },
            causa_interrupcion_otras_causas: {
                validators: {
                    callback: {
                        message: '',
                        callback: function(value, validator) {
                            var total = $('#id_total_interruptos_entidad').val(),
                                suma = parseInt(value) +
                                       parseInt($('#id_causa_interrupcion_rotura').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_piezas').val()) +
                                       parseInt($('#id_causa_interrupcion_accion_lluvia').val()) +
                                       parseInt($('#id_causa_interrupcion_falta_energia').val()) +
                                       parseInt($('#id_causa_interrupcion_orden_paralizacion_temporal').val()) +
                                       parseInt($('#id_causa_interrupcion_paralizacion_reparacion').val());

                            return total == suma;
                        }
                    }
                }
            }
            // actividad_indirectos: {
            //     validators: {
            //         callback: {
            //             message: '',
            //             callback: function(value, validator) {
            //                 alert(value);
            //
            //                 return 0;
            //             }
            //         }
            //     }
            // }
            // actividad_indirectos: {
            //     validators: {
            //         callback: {
            //             message: '',
            //             callback: function(value, validator) {
            //                 var total = $('#id_total_interruptos_entidad').val(),
            //                     suma = parseInt(value) +
            //                            parseInt($('#id_actividad_directos').val()) +
            //                            parseInt($('#id_actividad_todos').val());
            //
            //                 return total == suma;
            //             }
            //         }
            //     }
            // },
            // actividad_todos: {
            //     validators: {
            //         callback: {
            //             message: '',
            //             callback: function(value, validator) {
            //                 var total = $('#id_total_interruptos_entidad').val(),
            //                     suma = parseInt(value) +
            //                            parseInt($('#id_actividad_directos').val()) +
            //                            parseInt($('#id_actividad_indirectos').val());
            //
            //                 return total == suma;
            //             }
            //         }
            //     }
            // }
        }
    });
});