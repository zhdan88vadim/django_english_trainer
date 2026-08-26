curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "@dmin0"}' \
  -c cookies.txt \
  http://192.168.0.254:8090/api/auth/login/



  curl -X POST \
  -b cookies.txt \
  -d '{"delimiter": ";", "file_type": "csv"}' \  
  -F "file=@/media/vadim/c639b323-605b-440a-b6c8-f67f368cd6a5/learn/learn_audio_linux/english_audio_generator/data/oop.txt" \
  http://localhost:8090/api/upload/




!! not work   -F "delimiter=\;" \


  # curl -X POST \
  # -b cookies.txt \
  # -H "X-CSRFToken: $(awk '/csrftoken/ {print $7}' cookies.txt)" \
  # -H "Content-Type: multipart/form-data" \
  # -F "file=@/media/vadim/c639b323-605b-440a-b6c8-f67f368cd6a5/learn/learn_audio_linux/english_audio_generator/data/oop.txt" \
  # -F "delimiter=\;" \
  # -F "file_type=csv" \
  # http://localhost:8090/api/upload/



  curl -X POST \
  -b cookies.txt \
  -H "X-CSRFToken: $(awk '/csrftoken/ {print $7}' cookies.txt)" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/media/vadim/c639b323-605b-440a-b6c8-f67f368cd6a5/learn/learn_audio_linux/english_audio_generator/data/oop.txt" \
  -F "file_type=csv" \
  http://localhost:8090/api/upload/



  curl -X POST \
  -b cookies.txt \
  -H "X-CSRFToken: $(awk '/csrftoken/ {print $7}' cookies.txt)" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/media/vadim/c639b323-605b-440a-b6c8-f67f368cd6a5/learn/learn_audio_linux/english_audio_generator/data/python.txt" \
  -F "file_type=csv" \
  http://192.168.0.254:8090/api/upload/




  curl -X GET \
  -b cookies.txt \
  -H "X-CSRFToken: $(awk '/csrftoken/ {print $7}' cookies.txt)" \
http://localhost:8090/api/words/random/?count=3







http://192.168.0.53:8090/



curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "a@a.com", "password": "123"}' \
  -c cookies.txt \
  http://192.168.0.53:8090/api/auth/login/




  curl -X POST \
  -b cookies.txt \
  -H "X-CSRFToken: $(awk '/csrftoken/ {print $7}' cookies.txt)" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/media/vadim/c639b323-605b-440a-b6c8-f67f368cd6a5/learn/learn_audio_linux/english_audio_generator/data/python.txt" \
  http://192.168.0.53:8090/api/upload/

  curl -X POST \
  -b cookies.txt \
  -H "X-CSRFToken: $(awk '/csrftoken/ {print $7}' cookies.txt)" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/media/vadim/c639b323-605b-440a-b6c8-f67f368cd6a5/learn/learn_audio_linux/english_audio_generator/data/oop.txt" \
  http://192.168.0.53:8090/api/upload/