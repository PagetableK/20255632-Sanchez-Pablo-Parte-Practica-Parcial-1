from abc import ABC, abstractmethod
import random

class Recurso(ABC):
    def __init__(self, codigo_id):
        self.__codigo_id = codigo_id

    @abstractmethod
    def CalcularMulta():
        pass

    @abstractmethod
    def DescribirRecurso():
        pass

    @abstractmethod
    def TipoRecurso():
        pass

    @abstractmethod
    def ActualizarRetraso():
        pass

class PrestamoLibro(Recurso):
    def __init__(self, codigo_id):
        self.__codigo_id = codigo_id
        # --------------------------------------------------------> Modificar los días de retraso (self.__dias_retraso = x) para la validación "El promedio de multas excede $15"
        self.__dias_retraso = 0

    @property
    def CalcularMulta(self):
        return self.__dias_retraso * 2.50
    
    @property
    def DescribirRecurso(self):
        return f"Código del préstamo: {self.__codigo_id} - Días de retraso: {self.__dias_retraso}"
    
    @property
    def TipoRecurso(self):
        return "Libro"
    
    def ActualizarRetraso(self, dias_retraso):
        if dias_retraso > 0:
            self.__dias_retraso = dias_retraso
        else:
            raise ValueError("La cantidad de días de retraso no puede ser negativa")

class UsoSalaEstudio(Recurso):
    def __init__(self, codigo_id, cantidad_alumnos_espera):
        self.__codigo_id = codigo_id
        # --------------------------------------------------------> Modificar las horas de exceso (self.__horas_exceso = x) para la validación "El promedio de multas excede $15"
        self.__horas_exceso = 0
        self.__cantidad_alumnos_espera = cantidad_alumnos_espera
    
    @property
    def CalcularMulta(self):
        return self.__horas_exceso * self.__cantidad_alumnos_espera
    
    @property
    def DescribirRecurso(self):
        return f"Código del recurso: {self.__codigo_id} - Horas de exceso: {self.__horas_exceso}"
    
    @property
    def CantidadAlumnosEnEspera(self):
        return self.__cantidad_alumnos_espera
    
    @property
    def TipoRecurso(self):
        return "Sala"
    
    def ActualizarRetraso(self, horas_retraso):
        if horas_retraso > 0:
            self.__horas_exceso = horas_retraso
        else:
            raise ValueError("La cantidad de horas de exceso no puede ser negativa")
    
    def ActualizarAlumnosEspera(self, cantidad_alumnos):
        if cantidad_alumnos > 0:
            self.__cantidad_alumnos_espera = cantidad_alumnos
        else:
            raise ValueError("La cantidad de alumnos en espera no puede ser negativa")

class Bibliotecario():
    def __init__(self, nombre_empleado, codigo_usuario):
        self.__nombre_empleado = nombre_empleado
        self.__codigo_usuario = codigo_usuario

    @property
    def VerNombre(self):
        return self.__nombre_empleado

class RegistroAtencion():
    def __init__(self, codigo, carnet, nombre_empleado, codigo_usuario):
        self.__codigo = codigo
        self.__carnet = carnet
        self.__bibliotecario = Bibliotecario(nombre_empleado, codigo_usuario)
        self.__recursos = []
        self.__estado = "ACTIVO_NORMAL"
    
    def AgregarRecurso(self, tipo_recurso, codigo_id, cantidad_alumnos_espera = None):
        if len(self.__recursos) == 4:
            raise ValueError("Límite de recursos por atención alcanzado")
        
        if tipo_recurso.lower().strip() == "libro":
            self.__recursos.append(PrestamoLibro(codigo_id))
        elif tipo_recurso.lower().strip() == "sala":
            self.__recursos.append(UsoSalaEstudio(codigo_id, cantidad_alumnos_espera))
        else:
            print("El recurso no existe. Seleccione un recurso: Libro o Sala")
        
    @property
    def ConsultarRecursos(self):
        return tuple(self.__recursos)
    
    @property
    def CalcularTotalMultas(self):
        cantidad_multas = 0
        uso_sala_estudio_excedida = False
        total_multas = 0
        for recurso in self.__recursos:
            total_multas += recurso.CalcularMulta

            if total_multas != 0.0:
                cantidad_multas+=1

            if recurso.TipoRecurso == "Sala" and recurso.CantidadAlumnosEnEspera > 10:
                uso_sala_estudio_excedida = True
        
        if cantidad_multas == 0:
            promedio_multas = 0.0
        else:
            promedio_multas = total_multas / cantidad_multas

        if promedio_multas > 15 or (self.__bibliotecario.VerNombre.__contains__("AUX") and uso_sala_estudio_excedida):
            self.SuspenderCuenta
        
        return total_multas

    @property
    def ListarRecursos(self):
        print(f"\nCarnet del estudiante: {self.VerCarnet}")
        for recurso in self.__recursos:
            print(recurso.DescribirRecurso)

    @property
    def SuspenderCuenta(self):
        self.__estado = "CUENTA_SUSPENDIDA"

    @property
    def MostrarEstado(self):
        if self.__estado == "ACTIVO_NORMAL":
            print("\nLa cuenta está activa")
        else:
            print("\nLa cuenta ha sido suspendida")

    @property
    def VerCarnet(self):
        return self.__carnet

# ==========================================================================

# ========== Creando una nueva atención con recursos ============

atencion = RegistroAtencion(codigo="REG-2026-A", carnet="20255632", nombre_empleado="AUXLupita", codigo_usuario="20050007")

# ========== Agregando recursos ============
atencion.AgregarRecurso(tipo_recurso="libro", codigo_id="LIB-2026-06-20-0001")
atencion.AgregarRecurso(tipo_recurso="sala", codigo_id="SAL-2026-06-20-0001", cantidad_alumnos_espera=1)
atencion.AgregarRecurso(tipo_recurso="libro", codigo_id="LIB-2026-06-20-0002")

# --------------------------------------------------------> Modificar la cantidad de alumnos en espera
# (cantidad_alumnos_espera = 11) para la validación "El alumno tiene cargado una sala con más de 10 alumnos en lista de espera y el bibliotecario es personal auxiliar (AUX)"
atencion.AgregarRecurso(tipo_recurso="sala", codigo_id="SAL-2026-06-20-0002", cantidad_alumnos_espera = 10)

# ========== Mostrar estado de la cuenta =================
atencion.MostrarEstado

# ========== Consultando recursos y calculando total de multas de la atención ===========
print("\n============= Consultando recursos ===============")
print(atencion.ConsultarRecursos)
print("\n============= Cálculo del total de multas de los recursos ==============")
print(f"El total de multas es de ${atencion.CalcularTotalMultas}")

# ========== Listando los recursos agregado ===============
print("\n============= Lista de recursos ================")
atencion.ListarRecursos

# ========== Mostrar estado de la cuenta =================
atencion.MostrarEstado

# ========== Testeando la validación: límite de recursos =========
atencion.AgregarRecurso(tipo_recurso="libro", codigo_id="LIB-2026-06-20-0003")