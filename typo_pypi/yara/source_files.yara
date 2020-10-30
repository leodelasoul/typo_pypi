rule look_for_ips {

    strings:
        $re3 =  /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/
        $re5 = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b/
        $re6 = /(127\.[\d.]+|localhost)/
        $re7 = /(https?:\/\/(\.)?github.com)|(pypi.python)|(code.google)/
        $re8 = /#.*/

    condition:
       ($re3 and not $re6 ) or ($re5 and not $re7 and not ($re8 and $re5))

}


