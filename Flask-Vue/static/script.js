const { createApp } = Vue

createApp({
    data() {
      return {
        message: 'Hello ',
        newUsr: '',
        message2: 0,
        usuarios_lista: [],
        numero: null
      }
    },
    mounted() {
        fetch('/getData')
            .then(response => response.json())
            .then(data => {
                console.log(data)
                // Actualiza la interfaz de usuario con los datos recibidos
                this.usuarios_lista = data;
            })
            .catch(error => console.error('Error:', error));

        fetch('/getNumero')
            .then(response => response.json())
            .then(data => {
                // Actualiza la interfaz de usuario con los datos recibidos
                this.numero = data.num;
            })
            .catch(error => console.error('Error:', error));
    },
    methods: {
        increment(){
            this.numero++

            fetch('/actualizarBasedeDatos', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    // Actualiza la interfaz de usuario con los datos recibidos
                console.log(data)
                })
                .catch(error => console.error('Error:', error));
        },
        decrement(){
            this.numero--

            fetch('/actualizarBasedeDatosrest', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    // Actualiza la interfaz de usuario con los datos recibidos
                console.log(data)
                })
                .catch(error => console.error('Error:', error));
        },
        nuevousuario(){
            
            const nuevoUsuario = this.newUsr;
            fetch('/actualizarBasedeDatosusuarios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nombre: nuevoUsuario }),
            })
                .then(response => response.json())
                .then(data => {
                    // Actualiza la interfaz de usuario con los datos recibidos
                this.usuarios_lista.push(data)
                this.newUsr = ''
                })
                .catch(error => console.error('Error:', error));
        },
        eliminarusuario(id){
            
            const borrarUsuario = id;
            fetch('/actualizarBasedeDatoseliminar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'id': borrarUsuario }),
            })
                .then(response => response.json())
                .then(data => {
                    // Actualiza la interfaz de usuario con los datos recibidos
                this.usuarios_lista = this.usuarios_lista.filter((t) => t.id !== id)
                
                })
                .catch(error => console.error('Error:', error));
        }
    },
    delimiters: ['{','}']
}).mount('#app')

