document.addEventListener('DOMContentLoaded', function () {
  const tooltip = document.createElement('div');
  tooltip.className = 'event-tooltip';
  document.body.appendChild(tooltip);
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'pt',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,listWeek'
    },
    views: {
      listWeek: {
        buttonText: 'Lista'
      },
      dayGridMonth: {
        buttonText: 'Mês'
      }
    },
    fixedWeekCount: true,
    contentHeight: 'auto',
    editable: false,
    eventLimit: true,
    
    height: 'auto',
    eventSources: [
      {
        url: '../assets/calendar/aqw.json', 
        failure: () => alert('Falha ao carregar aqw.json')
      }
    ],

    eventDidMount: function(info) {
      
      const title = info.event.title.toLowerCase();
      const icon = document.createElement('span');
      icon.style.marginRight = '6px';

      if (title.includes('double rep')) {
        icon.innerHTML = '';
      } else if (title.includes('double exp')) {
        icon.innerHTML = '';
      } else if (title.includes('double gold')) {
        icon.innerHTML = '';
      } else if (title.includes('double class point')) {
        icon.innerHTML = '';
      }

      if (icon.innerHTML !== '') {
        info.el.querySelector('.fc-event-title')?.prepend(icon);
      }      
    
      // Tooltip hover
      const element = info.el;
      element.addEventListener('mouseenter', (e) => {
        const event = info.event;
        const start = event.start?.toLocaleDateString('pt-BR', {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      
        const end = event.end?.toLocaleDateString('pt-BR', {
          day: 'numeric',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      
        tooltip.innerHTML = `
          <h3>${event.title}</h3>
          ${event.extendedProps.description ? `<p>${event.extendedProps.description}</p>` : ''}
          <time>Início: ${start}</time>
          ${end ? `<time>Término: ${end}</time>` : ''}
        `;
      
        const rect = element.getBoundingClientRect();
        const tooltipWidth = tooltip.offsetWidth;
        const tooltipHeight = tooltip.offsetHeight;
        let top = rect.top + window.scrollY - tooltipHeight - 10;
        let left = rect.left + window.scrollX;
      
        if (top < window.scrollY) {
          top = rect.bottom + window.scrollY + 10;
        }
      
        if (left + tooltipWidth > window.scrollX + window.innerWidth) {
          left = window.scrollX + window.innerWidth - tooltipWidth - 10;
        }
      
        if (left < window.scrollX) {
          left = window.scrollX + 10;
        }
      
        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
        tooltip.classList.add('active');
      });

      // Adiciona o event listener para mouseleave
      element.addEventListener('mouseleave', () => {
        tooltip.classList.remove('active');
      });
    }
  });

  calendar.render();
});