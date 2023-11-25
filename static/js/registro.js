function registrarUsuario() {
    var nombre = $('#nombre').val();
    var appaterno = $('#appaterno').val();
    var apmaterno = $('#apmaterno').val();
    var correo = $('#correo').val();
    var contrasena = $('#contrasena').val();
 
    // Hacemos debug para ver si cachamos los datos
    console.log('Enviando datos de registro:');
    console.log('Nombre:', nombre);
    console.log('Apellido Paterno:', appaterno);
    console.log('Apellido Materno:', apmaterno);
    console.log('Correo electrónico:', correo);
 
   // Iniciamos con el Ajax 
    $.ajax({
         type: 'POST',
          url: '/registrar_usuario',
         data: {
             'nombre': nombre,
            'appaterno': appaterno,
            'apmaterno': apmaterno,
            'correo': correo,
            'contrasena': contrasena
         },
         success: function(data) {
         console.log('Respuesta del servidor:', data);
             $('#mensaje').text(data.mensaje);
         },
          error: function(error) {
         console.error('Error en la solicitud Ajax:', error);
          }
    });
 }