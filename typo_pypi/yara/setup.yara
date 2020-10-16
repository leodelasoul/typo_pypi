rule setup {

    strings:
        $re1 = "LOC"
        $re2 = "IP"
        $re3 =  /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/
        $re4 = "POST"
        $re5 = /https?:\/\/(\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b/
    condition:
        $re1 or $re2 or $re3 or ($re4 and $re5 )

}