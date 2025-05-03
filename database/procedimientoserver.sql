-- Crear usuario
CREATE PROCEDURE sp_CrearUsuario
    @NombreCompleto NVARCHAR(100),
    @Correo NVARCHAR(100),
    @Contrasena NVARCHAR(255),
    @Rol NVARCHAR(50),
    @IdDiscapacidad INT = NULL
AS
BEGIN
    INSERT INTO Usuarios (NombreCompleto, Correo, Contrasena, Rol, IdDiscapacidad)
    VALUES (@NombreCompleto, @Correo, @Contrasena, @Rol, @IdDiscapacidad);
END;

-- Leer usuario
CREATE PROCEDURE sp_ObtenerUsuario
    @IdUsuario INT
AS
BEGIN
    SELECT * FROM Usuarios WHERE IdUsuario = @IdUsuario;
END;

-- Actualizar usuario
CREATE PROCEDURE sp_ActualizarUsuario
    @IdUsuario INT,
    @NombreCompleto NVARCHAR(100),
    @Correo NVARCHAR(100),
    @Contrasena NVARCHAR(255),
    @Rol NVARCHAR(50),
    @IdDiscapacidad INT = NULL
AS
BEGIN
    UPDATE Usuarios
    SET NombreCompleto = @NombreCompleto,
        Correo = @Correo,
        Contrasena = @Contrasena,
        Rol = @Rol,
        IdDiscapacidad = @IdDiscapacidad
    WHERE IdUsuario = @IdUsuario;
END;

-- Eliminar usuario
CREATE PROCEDURE sp_EliminarUsuario
    @IdUsuario INT
AS
BEGIN
    DELETE FROM Usuarios WHERE IdUsuario = @IdUsuario;
END;


-- Crear discapacidad
CREATE PROCEDURE sp_CrearTipoDiscapacidad
    @Nombre NVARCHAR(100),
    @Descripcion NVARCHAR(255)
AS
BEGIN
    INSERT INTO Tipos_Discapacidad (Nombre, Descripcion)
    VALUES (@Nombre, @Descripcion);
END;

-- Leer
CREATE PROCEDURE sp_ObtenerTiposDiscapacidad
AS
BEGIN
    SELECT * FROM Tipos_Discapacidad;
END;

-- Actualizar
CREATE PROCEDURE sp_ActualizarTipoDiscapacidad
    @IdDiscapacidad INT,
    @Nombre NVARCHAR(100),
    @Descripcion NVARCHAR(255)
AS
BEGIN
    UPDATE Tipos_Discapacidad
    SET Nombre = @Nombre, Descripcion = @Descripcion
    WHERE IdDiscapacidad = @IdDiscapacidad;
END;

-- Eliminar
CREATE PROCEDURE sp_EliminarTipoDiscapacidad
    @IdDiscapacidad INT
AS
BEGIN
    DELETE FROM Tipos_Discapacidad WHERE IdDiscapacidad = @IdDiscapacidad;
END;

-- Crear vacante
CREATE PROCEDURE sp_CrearVacante
    @IdEmpresa INT,
    @Titulo NVARCHAR(100),
    @Descripcion NVARCHAR(MAX),
    @Requisitos NVARCHAR(MAX)
AS
BEGIN
    INSERT INTO Vacantes (IdEmpresa, Titulo, Descripcion, Requisitos)
    VALUES (@IdEmpresa, @Titulo, @Descripcion, @Requisitos);
END;

-- Leer
CREATE PROCEDURE sp_ObtenerVacantes
AS
BEGIN
    SELECT * FROM Vacantes;
END;

-- Actualizar
CREATE PROCEDURE sp_ActualizarVacante
    @IdVacante INT,
    @Titulo NVARCHAR(100),
    @Descripcion NVARCHAR(MAX),
    @Requisitos NVARCHAR(MAX)
AS
BEGIN
    UPDATE Vacantes
    SET Titulo = @Titulo, Descripcion = @Descripcion, Requisitos = @Requisitos
    WHERE IdVacante = @IdVacante;
END;

-- Eliminar
CREATE PROCEDURE sp_EliminarVacante
    @IdVacante INT
AS
BEGIN
    DELETE FROM Vacantes WHERE IdVacante = @IdVacante;
END;

-- Crear postulacion
-- Crear
CREATE PROCEDURE sp_CrearPostulacion
    @IdUsuario INT,
    @IdVacante INT
AS
BEGIN
    INSERT INTO Postulaciones (IdUsuario, IdVacante)
    VALUES (@IdUsuario, @IdVacante);
END;

-- Leer
CREATE PROCEDURE sp_ObtenerPostulaciones
AS
BEGIN
    SELECT * FROM Postulaciones;
END;

-- Actualizar estado
CREATE PROCEDURE sp_ActualizarEstadoPostulacion
    @IdPostulacion INT,
    @Estado NVARCHAR(50)
AS
BEGIN
    UPDATE Postulaciones
    SET Estado = @Estado
    WHERE IdPostulacion = @IdPostulacion;
END;

-- Eliminar
CREATE PROCEDURE sp_EliminarPostulacion
    @IdPostulacion INT
AS
BEGIN
    DELETE FROM Postulaciones WHERE IdPostulacion = @IdPostulacion;
END;

-- Crear curso
CREATE PROCEDURE sp_CrearCurso
    @Titulo NVARCHAR(100),
    @Descripcion NVARCHAR(MAX),
    @Accesibilidad NVARCHAR(100),
    @URLContenido NVARCHAR(255)
AS
BEGIN
    INSERT INTO Cursos (Titulo, Descripcion, Accesibilidad, URLContenido)
    VALUES (@Titulo, @Descripcion, @Accesibilidad, @URLContenido);
END;

-- Leer
CREATE PROCEDURE sp_ObtenerCursos
AS
BEGIN
    SELECT * FROM Cursos;
END;

-- Actualizar
CREATE PROCEDURE sp_ActualizarCurso
    @IdCurso INT,
    @Titulo NVARCHAR(100),
    @Descripcion NVARCHAR(MAX),
    @Accesibilidad NVARCHAR(100),
    @URLContenido NVARCHAR(255)
AS
BEGIN
    UPDATE Cursos
    SET Titulo = @Titulo, Descripcion = @Descripcion,
        Accesibilidad = @Accesibilidad, URLContenido = @URLContenido
    WHERE IdCurso = @IdCurso;
END;

-- Eliminar
CREATE PROCEDURE sp_EliminarCurso
    @IdCurso INT
AS
BEGIN
    DELETE FROM Cursos WHERE IdCurso = @IdCurso;
END;

---- Inscribir usuario en curso
CREATE PROCEDURE sp_InscribirCurso
    @IdCurso INT,
    @IdUsuario INT
AS
BEGIN
    INSERT INTO Cursos_Usuarios (IdCurso, IdUsuario)
    VALUES (@IdCurso, @IdUsuario);
END;

-- Ver inscripciones
CREATE PROCEDURE sp_ObtenerInscripcionesCurso
AS
BEGIN
    SELECT * FROM Cursos_Usuarios;
END;

-- Eliminar inscripción
CREATE PROCEDURE sp_EliminarInscripcionCurso
    @IdCurso INT,
    @IdUsuario INT
AS
BEGIN
    DELETE FROM Cursos_Usuarios WHERE IdCurso = @IdCurso AND IdUsuario = @IdUsuario;
END;


-- Crear indicador
CREATE PROCEDURE sp_CrearIndicador
    @IdUsuario INT,
    @Tipo NVARCHAR(100),
    @Valor DECIMAL(10,2)
AS
BEGIN
    INSERT INTO Indicadores (IdUsuario, Tipo, Valor)
    VALUES (@IdUsuario, @Tipo, @Valor);
END;

-- Obtener indicadores
CREATE PROCEDURE sp_ObtenerIndicadores
AS
BEGIN
    SELECT * FROM Indicadores;
END;

-- Eliminar indicador
CREATE PROCEDURE sp_EliminarIndicador
    @IdIndicador INT
AS
BEGIN
    DELETE FROM Indicadores WHERE IdIndicador = @IdIndicador;
END;



