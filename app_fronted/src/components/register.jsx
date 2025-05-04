import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

// SVG con colores aplicados directamente
const UserIcon = ({className}) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#D508E2" style={{width: '20px', height: '20px'}} className={className}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
  </svg>
);

const EnvelopeIcon = ({className}) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#D508E2" style={{width: '20px', height: '20px'}} className={className}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
  </svg>
);

const LockClosedIcon = ({className}) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#D508E2" style={{width: '20px', height: '20px'}} className={className}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
  </svg>
);

const RoleIcon = ({className}) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#D508E2" style={{width: '20px', height: '20px'}} className={className}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
  </svg>
);

const DisabilityIcon = ({className}) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#D508E2" style={{width: '20px', height: '20px'}} className={className}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
  </svg>
);

const EyeIcon = ({className}) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#D508E2" style={{width: '20px', height: '20px'}} className={className}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const EyeSlashIcon = ({className}) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#D508E2" style={{width: '20px', height: '20px'}} className={className}>
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
  </svg>
);

const Register = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    nombreCompleto: '',
    email: '',
    phone: '',
    password: '',
    confirm: '',
    rol: 'usuario',
    idDiscapacidad: '',
    country: 'COL+57',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: name === 'phone' ? value.replace(/\D/g, '') : value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validaciones básicas
    if (!form.nombreCompleto || !form.email || !form.phone || !form.password || !form.confirm || !form.idDiscapacidad) {
      return setError('Completa todos los campos obligatorios.');
    }
    
    if (form.password !== form.confirm) {
      return setError('Las contraseñas no coinciden.');
    }
    
    setError('');
    setLoading(true);
    
    // Preparar datos para enviar a la API
    const userData = {
      nombre_completo: form.nombreCompleto,
      correo: form.email,
      telefono: form.country.split('+')[1] + form.phone,
      contrasena: form.password,
      rol: form.rol,
      id_discapacidad: parseInt(form.idDiscapacidad),
      fecha_registro: new Date().toISOString().split('T')[0] // Formato YYYY-MM-DD
    };
    
    try {
      // Enviar datos a la API
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Error al registrar usuario');
      }
      
      // Registro exitoso
      alert('¡Registro exitoso! Ahora puedes iniciar sesión.');
      navigate('/'); // Redirigir a la página de inicio de sesión
      
    } catch (error) {
      setError(`Error: ${error.message}`);
      console.error('Error de registro:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'system-ui, -apple-system, sans-serif',
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '16px',
        boxShadow: '0 10px 25px rgba(0, 0, 0, 0.2)',
        width: '100%',
        maxWidth: '420px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '2rem',
        margin: '1.5rem',
      }}>
        <img
          src="/inkluazul-remove.png"
          alt="Logo InKlúIA"
          style={{
            width: '112px',
            height: 'auto',
            marginTop: '8px',
            marginBottom: '24px',
          }}
        />
        <h2 style={{
          fontSize: '1.875rem',
          fontWeight: '600',
          marginBottom: '1.5rem',
          color: '#002F50',
          textAlign: 'center',
        }}>Registro</h2>
        <form style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
          width: '100%',
        }} onSubmit={handleSubmit}>
          {/* Nombre Completo */}
          <div style={{ position: 'relative' }}>
            <div style={{ position: 'absolute', left: '12px', top: '14px' }}>
              <UserIcon />
            </div>
            <input
              type="text"
              name="nombreCompleto"
              placeholder="Nombre completo"
              value={form.nombreCompleto}
              onChange={handleChange}
              required
              style={{
                paddingLeft: '2.5rem',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                width: '100%',
                color: '#002F50',
              }}
            />
          </div>

          {/* Correo */}
          <div style={{ position: 'relative' }}>
            <div style={{ position: 'absolute', left: '12px', top: '14px' }}>
              <EnvelopeIcon />
            </div>
            <input
              type="email"
              name="email"
              placeholder="Correo electrónico"
              value={form.email}
              onChange={handleChange}
              required
              style={{
                paddingLeft: '2.5rem',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                width: '100%',
                color: '#002F50',
              }}
            />
          </div>

          {/* Teléfono */}
          <div style={{ display: 'flex' }}>
            <select
              name="country"
              value={form.country}
              onChange={handleChange}
              style={{
                padding: '0.75rem',
                backgroundColor: 'white',
                fontSize: '0.875rem',
                border: '1px solid #d1d5db',
                borderRight: '0',
                borderRadius: '0.375rem 0 0 0.375rem',
                color: '#002F50',
              }}
            >
              <option value="COL+57">COL+57</option>
              <option value="MEX+52">MEX+52</option>
              <option value="ARG+54">ARG+54</option>
              <option value="PER+51">PER+51</option>
              <option value="CHL+56">CHL+56</option>
              <option value="ECU+593">ECU+593</option>
            </select>
            <input
              type="tel"
              name="phone"
              placeholder="Número de teléfono"
              value={form.phone}
              onChange={handleChange}
              required
              style={{
                padding: '0.75rem',
                width: '100%',
                border: '1px solid #d1d5db',
                borderRadius: '0 0.375rem 0.375rem 0',
                color: '#002F50',
              }}
            />
          </div>

          {/* Contraseña */}
          <div style={{ position: 'relative' }}>
            <div style={{ position: 'absolute', left: '12px', top: '14px' }}>
              <LockClosedIcon />
            </div>
            <input
              type={showPassword ? 'text' : 'password'}
              name="password"
              placeholder="Contraseña"
              value={form.password}
              onChange={handleChange}
              required
              style={{
                paddingLeft: '2.5rem',
                paddingRight: '2.5rem',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                width: '100%',
                color: '#002F50',
              }}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              style={{
                position: 'absolute',
                right: '12px',
                top: '14px',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '0',
              }}
            >
              {showPassword ? <EyeSlashIcon /> : <EyeIcon />}
            </button>
          </div>

          {/* Confirmar contraseña */}
          <div style={{ position: 'relative' }}>
            <div style={{ position: 'absolute', left: '12px', top: '14px' }}>
              <LockClosedIcon />
            </div>
            <input
              type={showConfirm ? 'text' : 'password'}
              name="confirm"
              placeholder="Confirmar contraseña"
              value={form.confirm}
              onChange={handleChange}
              required
              style={{
                paddingLeft: '2.5rem',
                paddingRight: '2.5rem',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                width: '100%',
                color: '#002F50',
              }}
            />
            <button
              type="button"
              onClick={() => setShowConfirm(!showConfirm)}
              style={{
                position: 'absolute',
                right: '12px',
                top: '14px',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '0',
              }}
            >
              {showConfirm ? <EyeSlashIcon /> : <EyeIcon />}
            </button>
          </div>

          {/* ID Discapacidad */}
          <div style={{ position: 'relative' }}>
            <div style={{ position: 'absolute', left: '12px', top: '14px' }}>
              <DisabilityIcon />
            </div>
            <select
              name="idDiscapacidad"
              value={form.idDiscapacidad}
              onChange={handleChange}
              required
              style={{
                paddingLeft: '2.5rem',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                width: '100%',
                color: '#002F50',
                appearance: 'none',
                backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%23d1d5db'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E")`,
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'right 0.75rem center',
                backgroundSize: '1rem',
              }}
            >
              <option value="">Selecciona tipo de discapacidad</option>
              <option value="1">Física</option>
              <option value="2">Visual</option>
              <option value="3">Auditiva</option>
              <option value="4">Cognitiva</option>
              <option value="5">Psicosocial</option>
              <option value="6">Múltiple</option>
            </select>
          </div>

          {/* Error */}
          {error && <div style={{ color: '#ef4444', fontSize: '0.875rem', textAlign: 'center' }}>{error}</div>}

          {/* Botón */}
          <button
            type="submit"
            style={{
              background: 'linear-gradient(to right, #002F50, #D508E2)',
              color: 'white',
              padding: '0.75rem 1rem',
              borderRadius: '0.375rem',
              fontWeight: '600',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              transition: 'all 0.3s ease',
              width: '100%',
              border: 'none',
              cursor: 'pointer',
              marginTop: '0.5rem',
            }}
          >
            {loading ? 'Registrando...' : 'Registrarte'}
          </button>

          <p style={{
            fontSize: '0.875rem',
            textAlign: 'center',
            color: '#4b5563',
            marginTop: '1rem',
          }}>
            ¿Ya tienes cuenta?{' '}
            <Link to="/" style={{ color: '#002F50', fontWeight: '500', textDecoration: 'none' }}>Inicia sesión</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Register;