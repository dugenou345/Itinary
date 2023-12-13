FROM python:3.8

#WORKDIR /app
WORKDIR /

# Mise à jour de pip
RUN pip install --upgrade pip

# Copie des fichiers requirements.txt et installation des dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'application
COPY app.py .
#WORKDIR /app
#COPY app.py /app

# Print the contents of the /app directory again for verification
RUN ls -l /

# Print a message to indicate that app.py was copied
#CMD if [ -e "app.py" ]; then echo "app.py exists"; else echo "app.py does not exist"; fi


CMD ["python", "app.py"]

#CMD ["/bin/bash"]