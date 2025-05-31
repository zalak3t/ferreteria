from fastapi import APIRouter, HTTPException , Form
from app.database import get_conexion


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

#endpoints: GET, GET, POST, PUT, DELETE, PATCH
@router.get("/")
def obtener_usuarios():
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT rut, nombre, email, tipo FROM usuarios") 
        usuarios = []
        for rut, nombre, email, tipo in cursor:
            usuarios.append({
                "rut": rut,
                "nombre": nombre,
                "email": email,
                "tipo": tipo
            })
        cursor.close()
        cone.close()
        return {"usuarios": usuarios} 
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(ex)}")

@router.get("/{rut_buscar}")
def obtener_usuario(rut_buscar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT nombre, email, tipo FROM usuarios WHERE rut = :rut"
                       ,{"rut": rut_buscar})
        usuarios = cursor.fetchone()
        cursor.close()
        cone.close()
        if not usuarios:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "rut": rut_buscar,
            "nombre": usuarios[0],
            "email": usuarios[1],
            "tipo": usuarios[2]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(ex)}")

@router.post("/")
def agregar_usuario(
    rut: int = Form(...),
    nombre: str = Form(...),
    email: str = Form(...),
    tipo: str = Form(...),
    pass_: str = Form(...)
):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
            INSERT INTO usuarios (rut, nombre, email, pass, tipo)
            VALUES (:rut, :nombre, :email, :pass, :tipo)
        """, {
            "rut": rut,
            "nombre": nombre,
            "email": email,
            "pass": pass_,
            "tipo": tipo
        })
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario agregado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al agregar usuario: {str(ex)}")


@router.put("/{rut_actualizar}")
def actualizar_usuario(rut_actualizar:int, nombre:str, email:str, tipo:str):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("""
                UPDATE usuarios
                SET nombre = :nombre, email = :email, tipo = :tipo
                WHERE rut = :rut
        """, {"nombre":nombre, "email":email, "tipo":tipo , "rut":rut_actualizar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(ex)}")

@router.delete("/{rut_eliminar}")
def eliminar_usuario(rut_eliminar: int):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        cursor.execute("DELETE FROM usuarios WHERE rut = :rut"
                       ,{"rut": rut_eliminar})
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Usuario eliminado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(ex)}")


from typing import Optional

@router.patch("/{rut_actualizar}")
def actualizar_parcial(rut_actualizar:int, nombre:Optional[str]=None, email:Optional[str]=None, tipo:Optional[str]=None):
    try:
        if not nombre and not email and not tipo:
            raise HTTPException(status_code=400, detail="Debe enviar al menos 1 dato")
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"rut": rut_actualizar}
        if nombre:
            campos.append("nombre = :nombre")
            valores["nombre"] = nombre
        if email:
            campos.append("email = :email")
            valores["email"] = email
        if tipo:
            campos.append("tipo = :tipo")

        cursor.execute(f"UPDATE usuarios SET {', '.join(campos)} WHERE rut = :rut"
                       ,valores)
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        cone.commit()
        cursor.close()
        cone.close()        
        return {"mensaje": "Usuario actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(ex)}")