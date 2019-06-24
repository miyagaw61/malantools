$adapter = (Get-WmiObject Win32_NetworkAdapterConfiguration |
             where {$_.IPAddress -match "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"})
$ip_list = $adapter.IPAddress

foreach ($ip in $ip_list) {
    if ($ip -match "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}") {
        $ips = $ip.split(".")
        $dnsgw = $ips[0] + "." + $ips[1] + "." + $ips[2] + ".1"
        $adapter.SetGateways( $dnsgw )
        $adapter.SetDNSServerSearchOrder( $dnsgw )
        break
    }
}
