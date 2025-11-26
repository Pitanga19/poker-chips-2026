from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import List

# Clase base para excepciones personalizados
class CustomException(Exception):
    status_code = 500

    @staticmethod
    async def handler(request: Request, exc: 'CustomException'):
        return JSONResponse(
            status_code=exc.status_code,
            content={'msg': str(exc)},
        )

# Excepción de token inválido
class InvalidTokenException(CustomException):
    status_code = 401

# Excepción de contraseña incorrecta
class IncorrectPasswordException(CustomException):
    status_code = 401

# Excepción de usuario inactivo
class InactiveUserException(CustomException):
    status_code = 401

# Excepción de valor no encontrado
class NotFoundException(CustomException):
    status_code = 404

# Excepción de valor ya existente
class AlreadyExistsException(CustomException):
    status_code = 409

# Excepción de validación
class ValidationException(CustomException):
    status_code = 422

# Lista de excepciones personalizados
custom_exceptions: List[CustomException] = [
    CustomException,
    InvalidTokenException,
    IncorrectPasswordException,
    InactiveUserException,
    NotFoundException,
    AlreadyExistsException,
    ValidationException,
]

# Función para registrar los manejadores de excepciones personalizados
def register_custom_exceptions(app: FastAPI):
    for exception in custom_exceptions:
        app.add_exception_handler(exception, exception.handler)
