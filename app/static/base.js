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
        weekNumbers: false,
        navLinks: false,
        editable: false,
        eventLimit: false,
        firstDay: 1,
        timeFormat: 'H:mm',
        weekends: false,
        // events: [
        //     {
        //         title: 'ESSI39.2 - PERÍCIAS EM PERICULOSIDADE, INSALUBRIDADE E ACIDENTES DO TRABALHO (PRÁTICA)',
        //         start: segunda.add(10, 'hours'),
        //         end: segunda.add(2, 'hours')
        //     },
        //     {
        //         title: 'Click for Google',
        //         url: 'http://google.com/',
        //         start: '2018-03-28'
        //     }
        // ],
        eventRender: function (event, element) {
            element.append("<span class='closeon'>X</span>");
            element.find(".closeon").click(function () {
                var aux = localStorage.getItem("disciplinas");
                var obj = JSON.parse(aux);
                var i = 0;
                for (var x in obj) {
                    if (obj[i].title == event.title) {
                        obj.splice(i, 1);
                    }
                    i += 1;
                }
                $('#calendar').fullCalendar('removeEvents', event.id);
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
        }
        //     ,
        //     eventRender: function(event, element) {
        //       element.qtip({
        //         content: event.description
        //       });
        //     }
    });
});

function insereEvento(nome) {
    event = [
        {
            title: nome,
            start: moment().weekday(2).set({hour: 10, minute: 0, second: 0, millisecond: 0})
        }
    ];
    $('#calendar').fullCalendar('addEventSource', event);
    disciplinas.push(
        {title: nome, start: moment().weekday(2).set({hour: 10, minute: 0, second: 0, millisecond: 0})}
    );
    localStorage.setItem("disciplinas", JSON.stringify(disciplinas));
}