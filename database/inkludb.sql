CREATE DATABASE inkludb;
GO

USE inkludb;
GO

-- Tabla: Tipos de discapacidad
CREATE TABLE Tipos_Discapacidad (
    IdDiscapacidad INT PRIMARY KEY IDENTITY,
    Nombre NVARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(255)
);

-- Tabla: Usuarios
CREATE TABLE Usuarios (
    IdUsuario INT PRIMARY KEY IDENTITY,
    NombreCompleto NVARCHAR(100) NOT NULL,
    Correo NVARCHAR(100) UNIQUE NOT NULL,
    Contrasena NVARCHAR(255) NOT NULL,
    Rol NVARCHAR(50) CHECK (Rol IN ('Talento', 'Empresa', 'ONG')) NOT NULL,
    IdDiscapacidad INT NULL,
    FechaRegistro DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdDiscapacidad) REFERENCES Tipos_Discapacidad(IdDiscapacidad)
);

-- Tabla: Vacantes
CREATE TABLE Vacantes (
    IdVacante INT PRIMARY KEY IDENTITY,
    IdEmpresa INT NOT NULL,
    Titulo NVARCHAR(100),
    Descripcion NVARCHAR(MAX),
    Requisitos NVARCHAR(MAX),
    FechaPublicacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdEmpresa) REFERENCES Usuarios(IdUsuario)
);

-- Tabla: Postulaciones
CREATE TABLE Postulaciones (
    IdPostulacion INT PRIMARY KEY IDENTITY,
    IdUsuario INT NOT NULL,
    IdVacante INT NOT NULL,
    FechaPostulacion DATETIME DEFAULT GETDATE(),
    Estado NVARCHAR(50) DEFAULT 'Pendiente',
    FOREIGN KEY (IdUsuario) REFERENCES Usuarios(IdUsuario),
    FOREIGN KEY (IdVacante) REFERENCES Vacantes(IdVacante)
);

-- Tabla: Cursos
CREATE TABLE Cursos (
    IdCurso INT PRIMARY KEY IDENTITY,
    Titulo NVARCHAR(100),
    Descripcion NVARCHAR(MAX),
    Accesibilidad NVARCHAR(100),
    URLContenido NVARCHAR(255)
);

-- Tabla: Inscripciones a cursos
CREATE TABLE Cursos_Usuarios (
    IdCurso INT,
    IdUsuario INT,
    FechaInscripcion DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (IdCurso, IdUsuario),
    FOREIGN KEY (IdCurso) REFERENCES Cursos(IdCurso),
    FOREIGN KEY (IdUsuario) REFERENCES Usuarios(IdUsuario)
);

-- Tabla: Indicadores
CREATE TABLE Indicadores (
    IdIndicador INT PRIMARY KEY IDENTITY,
    IdUsuario INT,
    Tipo NVARCHAR(100),
    Valor DECIMAL(10,2),
    FechaRegistro DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdUsuario) REFERENCES Usuarios(IdUsuario)
);

