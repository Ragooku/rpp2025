from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Machine, MachineReading


class MachineListView(ListView):
    model = Machine
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        machines_with_readings = []
        for machine in context['machines']:
            last_reading = MachineReading.objects.filter(machine=machine).last()
            machines_with_readings.append({
                'machine': machine,
                'last_reading': last_reading
            })
        context['machines_with_readings'] = machines_with_readings
        return context


class MachineDetailView(DetailView):
    model = Machine
    template_name = 'machines/machine_detail.html'
    context_object_name = 'machine'


class MachineCreateView(CreateView):
    model = Machine
    template_name = 'machines/machine_form.html'
    fields = ['machine_number', 'manufacturer', 'model', 'installation_date', 'last_maintenance']
    success_url = reverse_lazy('machine-list')


class MachineUpdateView(UpdateView):
    model = Machine
    template_name = 'machines/machine_form.html'
    fields = ['machine_number', 'manufacturer', 'model', 'installation_date', 'last_maintenance']
    success_url = reverse_lazy('machine-list')


class MachineDeleteView(DeleteView):
    model = Machine
    template_name = 'machines/machine_confirm_delete.html'
    success_url = reverse_lazy('machine-list')