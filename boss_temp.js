var _T = _T || []; !
function() {
    var b, a = document.createElement("script");
    a.src = "https://static.zhipin.com/library/js/analytics/ka.js",
    b = document.getElementsByTagName("script")[0],
    b.parentNode.insertBefore(a, b)
} (),
function() {
    var e, f, g, h, a = function(a, b) {
        var c, d, e, f;
        "object" != typeof a && (a = [a]),
        c = document.getElementsByTagName("head").item(0) || document.documentElement,
        d = new Array,
        e = a.length - 1,
        f = function(g) {
            d[g] = document.createElement("script"),
            d[g].setAttribute("type", "text/javascript"),
            d[g].setAttribute("charset", "UTF-8"),
            d[g].onload = d[g].onreadystatechange = function() {
                this.onload = this.onreadystatechange = null,
                this.parentNode.removeChild(this),
                g != e ? f(g + 1) : "function" == typeof b && b()
            },
            d[g].setAttribute("src", a[g]),
            c.appendChild(d[g])
        },
        f(0)
    },
    b = function(a) {
        var b = new RegExp("(^|&)" + a + "=([^&]*)(&|$)"),
        c = window.location.search.substr(1).match(b);
        return null != c ? unescape(c[2]) : null
    },
    c = {
        get: function(a) {
            var b, c = new RegExp("(^| )" + a + "=([^;]*)(;|$)");
            return (b = document.cookie.match(c)) ? unescape(b[2]) : null
        },
        set: function(a, b, c, d, e) {
            var g, f = a + "=" + encodeURIComponent(b);
            c && (g = new Date(c).toGMTString(), f += ";expires=" + g),
            f = d ? f + ";domain=" + d: f,
            f = e ? f + ";path=" + e: f,
            document.cookie = f
        }
    };
    if (window.location.href, e = decodeURIComponent(b("seed")) || "", f = b("ts"), g = b("name"), h = decodeURIComponent(b("callbackUrl")), e && f && g) a("security-js/" + g + ".js",
    function() {
        var a = (new Date).getTime() + 2304e5,
        b = ".zhipin.com",
        d = "";
        try {
            d = (new ABC).z(e, parseInt(f))
        } catch(g) {
            _T.sendTracking("security_bridge_error_" + d)
        }
        if (d && h) {
            window.location.host.indexOf(".weizhipin.com") > -1 && (b = ".weizhipin.com"),
            c.set("__zp_stoken__", d, a, b, "/");
            try {
                _T.sendEvent("security_bridge_" + d),
                _T.sendTracking("security_bridge_" + d)
            } catch(g) {}
            window.location.href = h
        } else window.history.back()
    });
    else {
        try {
            _T.sendTracking("security_bridge_noseed_" + code)
        } catch(i) {}
        h ? window.location.href = h: window.history.back()
    }
} ();
