# Activo mi entorno base y mi env
& C:\ProgramData\Anaconda3\shell\condabin\conda-hook.ps1; conda activate base
& C:\ProgramData\Anaconda3\shell\condabin\conda-hook.ps1; conda activate nuevo2-env
# 2. Correr tools/request.ipynb para hacer el request a Ubidots.
& python Informe_semanal_v2\tools\request.py
#& C:\ProgramData\Anaconda3\python.exe Informe_semanal_v2\tools\request.py
# 4. Borrar los notebooks individuales por sede (main/notebooks/individual)
& Remove-Item 'Informe_semanal_v2\main\notebooks\individual\' -Recurse

#5. Replicar el modelo para cada sede usando tools/builder.ipynb
& python Informe_semanal_v2\tools\builder.py

#7. Borrar la carpeta main/\_build (o manipular la configuración de ejecución entre cache y force. Borrar funciona como hacer force)#
& Remove-Item 'Informe_semanal_v2\main\_build' -Recurse
# 10. Correr el comando: "jb build main" para compilar los notebooks
& jb build "Informe_semanal_v2\main"

