import React, { useState } from 'react';

function App() {
  // Состояние для хранения записей (изначально пусто)
  const [entries, setEntries] = useState([]);

  // Состояния для полей формы добавления
  const [date, setDate] = useState('');
  const [fullName, setFullName] = useState('');
  const [object, setObject] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [serialNumbers, setSerialNumbers] = useState('');

  // Генерация следующего ID (в реальном приложении ID будет приходить с бэкенда)
  const nextId = entries.length ? Math.max(...entries.map(e => e.id)) + 1 : 1;

  // Обработчик добавления новой записи
  const handleAddEntry = (e) => {
    e.preventDefault();
    if (!date || !fullName || !object || !phone || !email || !serialNumbers) {
      alert('Пожалуйста, заполните все поля');
      return;
    }
    const newEntry = {
      id: nextId,
      date,
      fullName,
      object,
      phone,
      email,
      serialNumbers,
    };
    setEntries([...entries, newEntry]);
    // Очистка формы
    setDate('');
    setFullName('');
    setObject('');
    setPhone('');
    setEmail('');
    setSerialNumbers('');
  };

  // Экспорт данных в CSV
  const exportToCSV = () => {
    const headers = ['Дата', 'ФИО', 'Объект', 'Телефон', 'Email', 'Заводские номера'];
    const rows = entries.map(entry => [
      entry.date,
      entry.fullName,
      entry.object,
      entry.phone,
      entry.email,
      entry.serialNumbers,
    ]);
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'support_requests.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Заявки технической поддержки</h1>

      {/* Форма добавления нового обращения */}
      <form onSubmit={handleAddEntry} style={{ marginBottom: '30px', border: '1px solid #ccc', padding: '15px', borderRadius: '5px' }}>
        <h2>Добавить новое обращение</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} placeholder="Дата" />
          <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="ФИО" />
          <input type="text" value={object} onChange={(e) => setObject(e.target.value)} placeholder="Объект" />
          <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Телефон" />
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
          <input type="text" value={serialNumbers} onChange={(e) => setSerialNumbers(e.target.value)} placeholder="Заводские номера" />
        </div>
        <button type="submit" style={{ marginTop: '15px', padding: '8px 16px', background: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Добавить
        </button>
      </form>

      {/* Таблица со списком обращений */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
          <thead>
            <tr style={{ background: '#f2f2f2' }}>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Дата</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>ФИО</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Объект</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Телефон</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Email</th>
              <th style={{ border: '1px solid #ddd', padding: '8px' }}>Заводские номера</th>
            </tr>
          </thead>
          <tbody>
            {entries.map(entry => (
              <tr key={entry.id}>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{entry.date}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{entry.fullName}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{entry.object}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{entry.phone}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{entry.email}</td>
                <td style={{ border: '1px solid #ddd', padding: '8px' }}>{entry.serialNumbers}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Кнопка экспорта в CSV */}
      <button onClick={exportToCSV} style={{ padding: '8px 16px', background: '#28a745', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
        Экспорт в CSV
      </button>
    </div>
  );
}

export default App;