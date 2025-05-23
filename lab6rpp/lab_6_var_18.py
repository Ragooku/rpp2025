import cherrypy
from peewee import *
from datetime import datetime

# Настроим подключение к базе данных
db = SqliteDatabase('measurements.db')

# Определим модель для базы данных
class BaseModel(Model):
    class Meta:
        database = db

class Measurement(BaseModel):
    measure_id = AutoField()  # Номер замера (автоинкрементируемый)
    vibration_frequency = FloatField()  # Частота вибраций
    power_consumption = FloatField()  # Потребляемая мощность
    temperature = FloatField()  # Температура
    machine_id = IntegerField()  # Номер станка
    reading = FloatField()  # Показания
    timestamp = DateTimeField(default=datetime.now)  # Дата и время замера

# Инициализируем базу данных и создаем таблицы
db.connect()
db.create_tables([Measurement], safe=True)

# Web-интерфейс на базе CherryPy
class WebApp:
    @cherrypy.expose
    def index(self):
        # Получаем все замеры из базы
        measurements = Measurement.select()
        
        # Формируем таблицу для отображения данных
        html = """
        <h1>Светофор</h1>
        <table border="1">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Кол-во машин</th>
                    <th>Проехало</th>
                    <th>Стоит машин</th>
                    <th>Номер светофора</th>
                    <th>Кол-во дней</th>
                    <th>Время включения</th>
                    <th>Действие</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Добавляем строки в таблицу
        for measure in measurements:
            html += f"""
            <tr>
                <td>{measure.measure_id}</td>
                <td>{measure.vibration_frequency}</td>
                <td>{measure.power_consumption}</td>
                <td>{measure.temperature}</td>
                <td>{measure.machine_id}</td>
                <td>{measure.reading}</td>
                <td>{measure.timestamp}</td>
                <td>
                    <a href="/delete_measurement/{measure.measure_id}">Delete</a>
                </td>
            </tr>
            """
        
        html += """
            </tbody>
        </table>
        <h2>Форма</h2>
        <form method="post" action="/add_measurement">
            Кол-во проехало: <input type="text" name="vibration_frequency"><br>
            Проехало машин: <input type="text" name="power_consumption"><br>
            Стоит машин: <input type="text" name="temperature"><br>
            Номер светофора: <input type="text" name="machine_id"><br>
            Кол-во дней: <input type="text" name="reading"><br>
            Время включения (YYYY-MM-DD HH:MM:SS): <input type="text" name="timestamp" placeholder="2025-05-23 15:30:00"><br>
            <input type="submit" value="Добавить запись">
        </form>
        """
        
        return html

    @cherrypy.expose
    def add_measurement(self, vibration_frequency, power_consumption, temperature, machine_id, reading, timestamp):
        # Преобразуем введенную дату и время в формат datetime
        try:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Преобразуем строку в datetime
        except ValueError:
            timestamp = datetime.now()  # Если ошибка, установим текущее время

        # Добавляем новый замер в базу
        if vibration_frequency and power_consumption and temperature and machine_id and reading:
            Measurement.create(
                vibration_frequency=float(vibration_frequency),
                power_consumption=float(power_consumption),
                temperature=float(temperature),
                machine_id=int(machine_id),
                reading=float(reading),
                timestamp=timestamp
            )
        raise cherrypy.HTTPRedirect("/")  # После добавления редирект на главную страницу

    @cherrypy.expose
    def delete_measurement(self, measure_id):
        # Удаляем замер из базы по ID
        measurement = Measurement.get(Measurement.measure_id == measure_id)
        measurement.delete_instance()
        raise cherrypy.HTTPRedirect("/")  # После удаления редирект на главную страницу

if __name__ == '__main__':
    # Настроим сервер CherryPy
    cherrypy.quickstart(WebApp())
