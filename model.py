from abc import ABC, abstractmethod
import random


cantidad_alumnos_espera = 10

class Recurso(ABC):
    def __init__(self, codigo_id):
        self.__codigo_id = codigo_id

    @abstractmethod
    def CalcularMulta():
        pass

    @abstractmethod
    def DescribirRecurso():
        pass

class PrestamoLibro(Recurso):
    def __init__(self, codigo_id):
        self.__codigo_id = codigo_id
        self.__dias_retraso = 1

    @property
    def CalcularMulta(self):
        return self.__dias_retraso * 2.50
    
    @property
    def DescribirRecurso(self):
        return f"Código del préstamo: {self.__codigo_id} - Días de retraso: {self.__dias_retraso}"

class UsoSalaEstudio(Recurso):
    def __init__(self, codigo_id):
        self.__codigo_id = codigo_id
        self.__horas_exceso = 5
    
    @property
    def CalcularMulta(self):
        
        return self.__horas_exceso * cantidad_alumnos_espera
    
    @property
    def DescribirRecurso(self):
        return f"Código del recurso: {self.__codigo_id} - Horas de exceso: {self.__horas_exceso}"

class Bibliotecario():
    def __init__(self, nombre_empleado, codigo_usuario):
        self.__nombre_empleado = nombre_empleado
        self.__codigo_usuario = codigo_usuario

class RegistroAtencion():
    def __init__(self, codigo, carnet, nombre_empleado, codigo_usuario):
        self.__codigo = codigo
        self.__carnet = carnet
        self.__bibliotecario = Bibliotecario(nombre_empleado, codigo_usuario)
        self.__recursos = []
    
    def AgregarRecurso(self, tipo_recurso, codigo_id):
        if len(self.__recursos) == 4:
            raise ValueError("Límite de recursos por atención alcanzado")
        
        if tipo_recurso.lower().strip() == "libro":
            self.__recursos.append(PrestamoLibro(codigo_id))
        elif tipo_recurso.lower().strip() == "sala":
            self.__recursos.append(UsoSalaEstudio(codigo_id))
        else:
            print("El recurso no existe. Seleccione un recurso: Libro o Sala")
        
    @property
    def ConsultarRecursos(self):
        return tuple(self.__recursos)
    
    @property
    def CalcularTotalMultas(self):
        return sum(recurso.CalcularMulta for recurso in self.__recursos)

    @property
    def ListarRecursos(self):
        for recurso in self.__recursos:
            print(recurso.DescribirRecurso)

# ==========================================================================

# ========== Creando una nueva atención con recursos ============

atencion = RegistroAtencion(codigo="REG-2026-A", carnet="20255632", nombre_empleado="Lupita", codigo_usuario="20050007")

# ========== Agregando recursos ============
atencion.AgregarRecurso(tipo_recurso="libro", codigo_id="LIB-2026-06-20-0001")
atencion.AgregarRecurso(tipo_recurso="sala", codigo_id="SAL-2026-06-20-0001")
atencion.AgregarRecurso(tipo_recurso="libro", codigo_id="LIB-2026-06-20-0002")
atencion.AgregarRecurso(tipo_recurso="sala", codigo_id="SAL-2026-06-20-0002")

# ========== Consultando recursos y calculando total de multas de la atención ===========
print("\n============= Consultando recursos ===============")
print(atencion.ConsultarRecursos)
print("\n============= Cálculo del total de multas de los recursos ==============")
print(atencion.CalcularTotalMultas)

# ========== Listando los recursos agregado ===============
print("\n============= Lista de recursos ================")
atencion.ListarRecursos

# ========== Testeando la validación: límite de recursos =========
atencion.AgregarRecurso(tipo_recurso="libro", codigo_id="LIB-2026-06-20-0003")