# Activo mi entorno base y mi env
#& C:/ProgramData/Anaconda3/shell/condabin/conda-hook.ps1; conda activate base
& /opt/anaconda3/shell/condabin/conda-hook.ps1; conda activate base
& /opt/anaconda3/shell/condabin/conda-hook.ps1; conda activate myenv
# 2. Correr tools/request.ipynb para hacer el request a Ubidots.

& python Informe_semanal_v2/tools/request.py


#& python Informe_semanal_v2/tools/request.py
# 4. Borrar los notebooks individuales por sede (main/notebooks/individual)
#& Remove-Item 'C:/Proyectos Digitalización/Bancolombia/CB_informes_Ubi/Informe_semanal_v2/main/notebooks/individual/*' -Recurse -Force
& Remove-Item "main/notebooks/individual/*" -Recurse -Force

# Paso adicional para cambiar a la carpeta deseada 
#Set-Location -Path 'C:/Proyectos Digitalización/Bancolombia/CB_informes_Ubi/Informe_semanal_v2'
Set-Location -Path 'CB_informes_Ubi/Informe_semanal_v2'

#5. Replicar el modelo para cada sede usando tools/builder.ipynb
cd "/Users/jpocampo/Library/CloudStorage/OneDrive-CELSIAS.AE.S.P/Proyectos Digitalización/Bancolombia/CB_informes_Ubi/Informe_semanal_v2/tools/"

python builder.py

#7. Borrar la carpeta main/_build (o manipular la configuración de ejecución entre cache y force. Borrar funciona como hacer force)#
#& Remove-Item 'C:/Proyectos Digitalización/Bancolombia/CB_informes_Ubi/Informe_semanal_v2/main/_build' -Recurse
cd "/Users/jpocampo/Library/CloudStorage/OneDrive-CELSIAS.AE.S.P/Proyectos Digitalización/Bancolombia/CB_informes_Ubi/Informe_semanal_v2/"

& Remove-Item  'main/_build' -Recurse -Force


# 10. Correr el comando: "jb build main" para compilar los notebooks
#& jb build "C:/Proyectos Digitalización/Bancolombia/CB_informes_Ubi/Informe_semanal_v2/main"
& jb build 'main'