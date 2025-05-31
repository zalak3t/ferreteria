const express = require('express')
const oracledb = require('oracledb')

const app = express()
const puerto = 3000
const dbConfig = {
    user:'db',
    password: 'db',
    connectString:'localhost/orcl'
}

/*const API_KEY ='.clave123'

function validarApiKey(req,res){
    const apiKey = req.headers['x-api-key']
    if(!apiKey || apiKey !== API_KEY){
        res.status(401).json({error: "apikey no entregada o incorrecta"})
    }
}*/

app.use(express.json())

app.get('/', (req,res) => {
    res.status(200).json({mensaje: "api express productos"})
})

app.get('/productos',/* validarApiKey,*/ async (req,res) => {
    let cone
    try {
        cone= await oracledb.getConnection(dbConfig)
        const result = await cone.execute("select * from productos")
        res.status(200).json(result.rows.map(row => ({
            codigo_producto: row[0],
            marca: row[1],
            codigo: row[2],
            nombre: row[3],
            imagen: row[4],
            precio: row[5],
            tipo: row[6]
        })))
    } catch (ex) {
        res.status(500).json({error: ex.message})
    } finally{
        if (cone) cone.close()
    }
})

app.get('/productos/:codigo_producto', async (req, res) => {
    let cone
    const codigo_producto = req.params.codigo_producto
    try {
        cone = await oracledb.getConnection(dbConfig)
        const result = await cone.execute(
            'SELECT * FROM productos WHERE codigo_producto = :codigo_producto', [codigo_producto]
        )
        if(result.rows.length===0){
            res.status(404).json({mensaje: "Producto no encontrado"})
        }else{
            const row = result.rows[0]
            res.json({
                codigo_producto: row[0],
                marca: row[1],
                codigo: row[2],
                nombre: row[3],
                imagen: row[4],
                precio: row[5],
                tipo: row[6]
            })
        }
    } catch (error) {
        res.status(500).json({error: error.message})
    } finally {
        if (cone) cone.close()
    }
})

app.post('/productos', async (req, res) => {
    let cone
    const {codigo_producto, marca, codigo, nombre, imagen, precio, tipo} = req.body
    try {
        cone = await oracledb.getConnection(dbConfig)
        await cone.execute(
            `INSERT INTO productos
             VALUES(:codigo_producto, :marca, :codigo, :nombre, :imagen, :precio, :tipo)`
            ,{codigo_producto, marca, codigo, nombre, imagen, precio, tipo}
            ,{autoCommit: true}
        )
        res.status(201).json({mensaje: "Producto creado"})
    } catch (error) {
        res.status(500).json({error: error.message})
    } finally {
        if (cone) cone.close()
    }
})

app.put('/productos/:codigo_producto', async(req, res) => {
    let cone
    const codigo_producto = req.params.codigo_producto
    const {marca, codigo, nombre, imagen, precio, tipo} = req.body
    try {
        cone = await oracledb.getConnection(dbConfig)
        const result = await cone.execute(
            `UPDATE productos
            SET marca = :marca, codigo = :codigo, nombre = :nombre, 
                imagen = :imagen, precio = :precio, tipo = :tipo
            WHERE codigo_producto = :codigo_producto`
            ,{codigo_producto, marca, codigo, nombre, imagen, precio, tipo}
            ,{autoCommit: true}
        )
        if(result.rowsAffected===0){
            res.status(404).json({mensaje: "Producto no encontrado"})
        }else{
            res.json({mensaje: 'Producto actualizado'})
        }
    } catch (error) {
        res.status(500).json({error: error.message})
    } finally {
        if (cone) cone.close()
    }
})

app.delete('/productos/:codigo_producto', async (req, res) => {
    let cone
    const codigo_producto = req.params.codigo_producto
    try {
        cone = await oracledb.getConnection(dbConfig)
        const result = await cone.execute(
            `DELETE FROM productos
            WHERE codigo_producto = :codigo_producto`
            ,[codigo_producto]
            ,{autoCommit: true}
        )
        if(result.rowsAffected===0){
            res.status(404).json({mensaje: "Producto no encontrado"})
        }else{
            res.json({mensaje: "Producto eliminado"})
        }
    } catch (error) {
        res.status(500).json({error: error.message})
    } finally {
        if (cone) cone.close()
    }
})

app.patch('/productos/:codigo_producto', async(req, res) => {
    let cone
    const codigo_producto = req.params.codigo_producto
    const {marca, codigo, nombre, imagen, precio, tipo} = req.body
    try {
        cone = await oracledb.getConnection(dbConfig)
        let campos = []
        let valores = {}
        if (marca !== undefined){
            campos.push('marca = :marca')
            valores.marca = marca
        }
        if(codigo !== undefined){
            campos.push('codigo = :codigo')
            valores.codigo = codigo
        }
        if(nombre !== undefined){
            campos.push('nombre = :nombre')
            valores.nombre = nombre
        }
        if(imagen !== undefined){
            campos.push('imagen = :imagen')
            valores.imagen = imagen
        }
        if(precio !== undefined){
            campos.push('precio = :precio')
            valores.precio = precio
        }
        if(tipo !== undefined){
            campos.push('tipo = :tipo')
            valores.tipo = tipo
        }
        if(campos.length===0){
            res.status(400).json({mensaje: 'No se enviaron campos para actualizar'})
        }
        valores.codigo_producto = codigo_producto
        const sql = `UPDATE productos SET ${campos.join(', ')} WHERE codigo_producto = :codigo_producto`
        const result = await cone.execute(
            sql, valores, {autoCommit: true}
        )
        if(result.rowsAffected===0){
            res.status(404).json({mensaje: "Producto no existe"})
        }else{
            res.json({mensaje: "Producto actualizado parcialmente"})
        }
    } catch (error) {
        res.status(500).json({error: error.message})
    } finally {
        if (cone) cone.close()
    }
})

app.listen(puerto, ()=>{
    console.log(`api escuchando puerto ${puerto}`);
})

