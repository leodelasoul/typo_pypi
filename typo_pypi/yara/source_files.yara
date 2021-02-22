rule look_for_ips {

    strings:
        $re3 =  /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/
        $re4 = /\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b/
        $re6 = /(127\.[\d.]+|localhost|0.0.0.0)/
        $re7 = /(https?:\/\/(\.)?github.com)|(pypi.python)|(code.google)|(googleapis|google)|(pypi.org)/
  condition:

    $re3 and not  $re7 and not $re4 and not $re6  and not (external1 matches /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/)

}


rule look_for_ips_and_not_whitelists {

    strings:
        $re5 = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b/
        $re7 = /(https?:\/\/(\.)?github.com)|(pypi.python)|(code.google)|(googleapis|google)|(pypi.org)/
        $re8 = /#.*/
        $re9 = /(\''')(.*\n*)(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)/
        $re10 = /(\#)(.*\n*)(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)/


    condition:

      $re5 and not $re7 and not ($re8 and $re5) and not (external matches /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b/) and not $re9 and not $re10

}
