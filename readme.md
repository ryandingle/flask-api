# Requirements
use python 3.8.x

# INSTRUCTION ON RUNNING THIS FLASK API APPLLICATION
`Using Virtual Environment for Python Packages Installation`

install virtualenv wrapper
`pip install virtualenv`

install python dependencies using virtualenv wrapper.
go to application root directory
1 `virtualenv env -p python3`
2 `source env/bin/activate`
3 `pip install -r requirements.txt`
run the application
1 `bash run.sh`

# USE POSTMAN for API ENDPOINT TESTING
# API ENDPOINTS
`notes: always add user_id get parameters on each request on the api resources /api/v1/list, /api/v1/cards, /api/v1/comments`
`Registered Test User are having id 1 as member and id 2 as admin`
`ex. http://localhost:5000/api/v1/lists/?user_id=1`

`users`
`/api/v1/users/` - GET
`/api/v1/create/` - POST form params = username,email,password,type(`admin`,`member`)

`auth`
`/api/v1/auth/signin/` - POST form params = email, password

`list` - before creating list, please add users both 'admin' and 'member'
`/api/v1/lists/?user_id=<list_id>` - GET
`/api/v1/lists/create/?user_id=<id>` - POST form params = title, assigned_member(leave blank if no value, but must be present on the request)
`/api/v1/lists/show/<list_id>/?user_id=<id>` - GET
`/api/v1/lists/update/<list_id>/?user_id=<id>` - POST form params = title, assigned_member(leave blank if no value, but must be present on the request)
`/api/v1/lists/member_assignment/<list_id>/?user_id=<id>` - POST form params = action(`assing`,`unassign`), member_id
`/api/v1/lists/delete/<list_id>/?user_id=<id>` - POST


`card` - to create cards, list must be required
`/api/v1/cards/?user_id=<id>` - GET
`/api/v1/cards/create/?user_id=<id>` - POST form params = title, description, list_id
`/api/v1/cards/show/<card_id>/?user_id=<id>` - GET
`/api/v1/cards/update/<card_id>/?user_id=<id>` - POST form params = title, description
`/api/v1/licardsst/delete/<card_id>/?user_id=<id>` - POST


`comments` - to create comments, cards must be present
`/api/v1/comments/?card_id=<card_id>&user_id=<id>` - GET
`/api/v1/comments/create/?user_id=<id>` - POST form params = body, card_id, list_id, is_reply_from(`id of main comment if is reply on the comment`)
`/api/v1/comments/show/<comment_id>/?user_id=<id>` - GET
`/api/v1/comments/update/<comment_id>/?user_id=<id>` - POST form params = body,
`/api/v1/comments/delete/<comment_id>/?user_id=<id>` - POST