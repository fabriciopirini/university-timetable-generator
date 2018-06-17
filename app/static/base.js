"use strict";
const segunda = moment().weekday(1).set({hour: 0, minute: 0, second: 0, millisecond: 0});
var disciplinas = [];
// console.log(segunda)
$(function () {

    $('#calendar').fullCalendar({
        defaultView: 'agendaWeek',
        height: 'auto',
        allDaySlot: false,
        columnHeaderFormat: 'dddd',
        minTime: '07:00:00',
        maxTime: '23:30:00',
        slotDuration: '00:55:00',
        slotLabelFormat: 'H:mm',
        eventBackgroundColor: '#9BD1E9',
        slotEventOverlap: false,
        nowIndicator: false,
        header: {
            left: '',
            center: 'title',
            right: ''
        },
        defaultDate: moment().weekday(1),
        weekNumbers: false,
        navLinks: false,
        editable: false,
        eventLimit: false,
        firstDay: 1,
        timeFormat: 'H:mm',
        weekends: false,
        events: [
            // {
            //     id: Math.floor(Math.random() * (100000 - 1) + 1).toString(),
            //     title: 'ESSI39.2 - PERÍCIAS EM PERICULOSIDADE, INSALUBRIDADE E ACIDENTES DO TRABALHO (PRÁTICA)',
            //     start: segunda.add(10, 'hours'),
            //     end: segunda.add(2, 'hours')
            // }
            // ,{
            //     title: 'Click for Google',
            //     url: 'http://google.com/',
            //     start: '2018-03-28'
            // }
        ],
        eventRender: function (event, element) {
            element.append("<span class='closeon'>X</span>");
            element.find(".closeon").click(function () {
                var aux = localStorage.getItem("disciplinas");
                var obj = JSON.parse(aux);
                var i = 0;
                while(i < obj.length){
                    if (obj[i].id == event.id) {
                        obj.splice(i, 1);
                    }
                    i += 1;
                }
                // console.log(event.id);
                $('#calendar').fullCalendar('removeEvents', event._id);
                localStorage.setItem("disciplinas", JSON.stringify(obj));
            });
        },
        eventMouseover: function (calEvent, jsEvent) {
            var tooltip = '<div class="tooltipevent" style="border-radius: 0.2em;border: 0.125em solid #84AE65;padding:0.5em;width:12.5em;height:auto;background:#B5EF8A;position:absolute;z-index:10001;">' + calEvent.title + '</div>';
            var $tooltip = $(tooltip).appendTo('body');

            $(this).mouseover(function (e) {
                $(this).css('z-index', 10000);
                $tooltip.fadeIn('500');
                $tooltip.fadeTo('10', 1.9);
            }).mousemove(function (e) {
                $tooltip.css('top', e.pageY + 10);
                $tooltip.css('left', e.pageX + 20);
            });
        },

        eventMouseout: function (calEvent, jsEvent) {
            $(this).css('z-index', 8);
            $('.tooltipevent').remove();
        },

        eventAfterRender:function( event, element, view ) {
            $(element).attr("id","event_id_"+event._id);
        }
    });

    var eventosPassados = JSON.parse(localStorage.getItem("disciplinas"));
    $('#calendar').fullCalendar('addEventSource', eventosPassados, true);
});

function formataHorario(horario) {
    var posDias = [
      ["2", "Seg"],
      ["3", "Ter"],
      ["4", "Qua"],
      ["5", "Qui"],
      ["6", "Sex"]
    ];
    var posHorarios = [
      ["1", "7:00"],
      ["2", "7:55"],
      ["3", "8:50"],
      ["4", "10:10"],
      ["5", "11:05"],
      ["6", "13:30"],
      ["7", "14:25"],
      ["8", "15:45"],
      ["9", "16:40"],
      ["10", "17:35"],
      ["11", "19:00"],
      ["12", "19:50"],
      ["13", "21:00"],
      ["14", "21:50"],
      ["15", "22:40"]
    ];
    var dias, horas;
    if (horario.search("M") > -1) {
      dias = horario.split("M")[0];
      horas = horario.split("M")[1];
      // for (var i = 0; i < dias.length; i++) {
      //    moment dias[i] CONTINUAR AQUI!!!!!
      //}
    }
    // else if (horario.search("T") > -1) {
    //   horario.split("T");
    // }
    // else if (horario.search("N") > -1) {
    //   horario.split("N");
    // }
}

function insereEvento(nome) {
    var idgerado = Math.floor(Math.random() * (100000 - 1) + 1).toString();
    event = [
        {
            id: idgerado,
            title: nome,
            start: moment().weekday(2).set({hour: 10, minute: 0, second: 0, millisecond: 0})
        }
    ];
    $('#calendar').fullCalendar('addEventSource', event, true);
    console.log("Disciplina " + nome + " inserida. ID: " + idgerado);

    disciplinas.push(
        {
            id: idgerado,
            title: nome,
            start: moment().weekday(2).set({hour: 10, minute: 0, second: 0, millisecond: 0})
        }
    );
    localStorage.setItem("disciplinas", JSON.stringify(disciplinas));
}
