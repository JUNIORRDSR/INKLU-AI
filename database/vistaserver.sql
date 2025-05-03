CREATE VIEW vw_VacantesConEmpresas AS
SELECT 
    V.IdVacante,
    V.Titulo,
    V.Descripcion,
    V.FechaPublicacion,
    E.NombreCompleto AS Empresa
FROM Vacantes V
JOIN Usuarios E ON V.IdEmpresa = E.IdUsuario
WHERE E.Rol = 'Empresa';

CREATE VIEW vw_PostulacionesDetalle AS
SELECT 
    P.IdPostulacion,
    U.NombreCompleto AS Talento,
    V.Titulo AS Vacante,
    P.Estado,
    P.FechaPostulacion
FROM Postulaciones P
JOIN Usuarios U ON P.IdUsuario = U.IdUsuario
JOIN Vacantes V ON P.IdVacante = V.IdVacante;

CREATE VIEW vw_CursosInscritos AS
SELECT 
    CU.IdCurso,
    C.Titulo,
    CU.IdUsuario,
    U.NombreCompleto,
    CU.FechaInscripcion
FROM Cursos_Usuarios CU
JOIN Cursos C ON CU.IdCurso = C.IdCurso
JOIN Usuarios U ON CU.IdUsuario = U.IdUsuario;

CREATE VIEW vw_IndicadoresUsuarios AS
SELECT 
    I.IdIndicador,
    U.NombreCompleto,
    I.Tipo,
    I.Valor,
    I.FechaRegistro
FROM Indicadores I
JOIN Usuarios U ON I.IdUsuario = U.IdUsuario;
