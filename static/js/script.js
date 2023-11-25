function verificarLogin() {
    var email = $('#email').val();
    var contrasena = $('#contrasena').val();

    $.ajax({
        type: 'POST',
         url: '/login',
        data: { 'email': email, 'contrasena': contrasena },
     success: function(data) {
	    console.log('Respuesta del servidor:', data);
            
            // if (data.resultado === 1) {
	    if (data.resultado === 'Inicio de sesión exitoso') {
                console.log('Inicio de sesión exitoso.');
                $('#resultado').text('Inicio de sesión exitoso.');

		// Redirigir a la página home después de 1 segundo
		// alterntiva porque no funciono el redirect en flask
                setTimeout(function() {
                   window.location.href = '/home';
                }, 1000);
            } else {
                console.log('Inicio de sesión fallido.');
                $('#resultado').text('Inicio de sesión fallido.');
            }
        },
        error: function(error) {
            console.error('Error en la solicitud Ajax:', error);
        }
    });
}
