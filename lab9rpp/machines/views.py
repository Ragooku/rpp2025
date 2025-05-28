from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Machine, MachineReading


class MachineListView(LoginRequiredMixin, ListView):
    model = Machine
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        machines_with_readings = []

        for machine in context['machines']:
            last_reading = MachineReading.objects.filter(machine=machine).order_by('-timestamp').first()
            machines_with_readings.append({
                'machine': machine,
                'last_reading': last_reading
            })

        context['machines_with_readings'] = machines_with_readings
        profile = getattr(self.request.user, 'profile', None)
        context['user_role'] = getattr(profile, 'role', None)
        context['can_add_reading'] = profile and profile.role and profile.role.name in ['Оператор',
                                                                                        'Начальник']
        return context


class MachineDetailView(LoginRequiredMixin, DetailView):
    model = Machine
    template_name = 'machines/machine_detail.html'
    context_object_name = 'machine'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['readings'] = MachineReading.objects.filter(
            machine=self.object
        ).order_by('-timestamp')[:5]

        profile = getattr(self.request.user, 'profile', None)
        context['can_edit'] = profile and profile.role and profile.role.name == 'Начальник'
        context['can_add_reading'] = profile and profile.role and profile.role.name in ['Оператор',
                                                                                        'Начальник']
        context['can_delete_reading'] = profile and profile.role and profile.role.name == 'Начальник'
        return context


class MachineCreateView(LoginRequiredMixin, CreateView):
    model = Machine
    template_name = 'machines/machine_form.html'
    fields = ['machine_number', 'manufacturer', 'model',
              'installation_date', 'last_maintenance']
    success_url = reverse_lazy('machine-list')

    def dispatch(self, request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not (profile and profile.role and profile.role.name == 'Начальник'):
            raise PermissionDenied("Только начальник может добавлять светофоры")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class MachineUpdateView(LoginRequiredMixin, UpdateView):
    model = Machine
    template_name = 'machines/machine_form.html'
    fields = ['machine_number', 'manufacturer', 'model',
              'installation_date', 'last_maintenance']
    success_url = reverse_lazy('machine-list')

    def dispatch(self, request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not (profile and profile.role and profile.role.name == 'Начальник'):
            raise PermissionDenied("Только начальник может редактировать светофоры")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MachineDeleteView(LoginRequiredMixin, DeleteView):
    model = Machine
    template_name = 'machines/machine_confirm_delete.html'
    success_url = reverse_lazy('machine-list')

    def dispatch(self, request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not (profile and profile.role and profile.role.name == 'Начальник'):
            raise PermissionDenied("Только начальник может удалять светофоры")
        return super().dispatch(request, *args, **kwargs)


class ReadingCreateView(LoginRequiredMixin, CreateView):
    model = MachineReading
    template_name = 'machines/reading_form.html'
    fields = ['vibration_frequency', 'power_consumption', 'temperature', 'timestamp']

    def get_success_url(self):
        return reverse_lazy('machine-detail', kwargs={'pk': self.kwargs['machine_pk']})

    def dispatch(self, request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not (profile and profile.role and profile.role.name in ['Оператор', 'Начальник']):
            raise PermissionDenied("Только оператор или начальник могут добавлять показания")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.machine_id = self.kwargs['machine_pk']
        form.instance.operator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = Machine.objects.get(pk=self.kwargs['machine_pk'])
        return context


class ReadingDeleteView(LoginRequiredMixin, DeleteView):
    model = MachineReading
    template_name = 'machines/reading_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('machine-detail', kwargs={'pk': self.object.machine.pk})

    def dispatch(self, request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not (profile and profile.role and profile.role.name == 'Начальник'):
            raise PermissionDenied("Только начальник может удалять показания")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.object.machine
        return context