# Django-question

### Using Docker:  
```sudo docker-compose build```  
```sudo docker-compose up``` 

PostgresDB not working right now. Eventually it will.

## Paths :
- `/api/registration` 
  - `post` - Create a new user.
- `/api/login` 
  - `post` - Login user. 
- `/api/token_auth` 
  - `post` - Authenticate user using jwt token.
- `/api/profile`  
  - `get`- Get your personal info.  
- `/api/profile/update_user`
  - `put`- Updates your personal info.

Some links required to be Authenticated down below.
- `/api/questions`   
  - `get` - View a questions list.  
  - `post` - Create new questions.  
- `/api/questions/<int:id>`
  - `get` - Get a question and all answers.  
  - `delete` - Remove a question and all answers.  
- `/api/questions/<int:id>/answers`
  - `post` - Create new answer to question.
- `/api/answers/<int:id>`
  - `get` - Get answer.  
  - `delete` - Remove answer.  
