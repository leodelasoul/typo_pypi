rule setup {

    strings:
        $re1 = "LOC"
        $re2 = "IP"
        $re3 =  /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/
    condition:
        $re1 or $re2 or $re3

}