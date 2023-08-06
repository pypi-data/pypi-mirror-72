# replit-db-client
a client for repl db for python


# docs
### import
`import replitdb`
### define the client
`client = replitdb.Client`
### edit keys
##### adding
`client.add(name=value)` note you can add multiple at one time just add a comma and another `name=value` (returns nothing)
##### removing
`client.remove(name)` like before just add more seperated by commas todo more (returns nothing)
##### clearing
`client.wipe` WARNING THIS CANNOT BE UNDONE (returns nothing)
### viewing keys
##### list keys
`client.list(prefix)` list all keys with that in the begining of there name (returns list)
`client.list_multiple(prefix)` you can add more seperated by commas (returns dict)
##### viewing keys
`client.view(name)` returns  the value
`client.view_multiple(name)` add more seperated by commas (returns dict)
##### view all keys
`client.all` returns all key names (returns list)
##### view all data
`client.all_dict` (returns dict)
