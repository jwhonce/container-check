(*
Module: syslog-ng
    Parses syslog-ng configuration files.

Author:
    Jhon Honce              <jhonce@redhat.com>

About: Licence
    This file is licensed under the LGPL v2+, like the rest of Augeas.

About: Lens Usage
    Sample usage of this lens in augtool
        * print all
           print /files/etc/syslog-ng.conf

About: Configuration files
    This lens applies to /etc/syslog-ng.conf and /etc/syslog-ng.d/*.
    See <filter>.
 *)

module Syslog_ng =
   autoload xfm

   (* bits and bobs *)
   let at       = Util.del_str "@"
   let colon    = Util.del_str ":"
   let semi     = Util.del_str ";"
   let comment  = Util.comment
   let empty    = Util.empty
   let eol      = Util.eol
   let indent   = Util.indent
   let quote    = Quote.quote

   let id       = /[a-zA-Z0-9_.-]+/
   let name     = /[^#= \n\t{}()\/]+/

   let lbracket = del /[ \t\n]*\{([ \t\n]*\n)?/ " {"
   let rbracket = del /[ \t]*\}/ "}"
   let lparan   = del /[ \t\n]*\(/ " ("
   let rparan   = del /[ \t]*\)/ ")"
   let eq       = indent . Util.del_str "=" . indent

   let value_to_eol = store ( /[^\n]*/ - /([ \t][^\n]*|[^\n]*[ \t])/ )
   let value_quoted = del "\"" "\"" . store /^"\n]+/ . del "\"" "\""
   let option_value = key id . lparan . store /[^ \t\n#;()]+/ . rparan . semi . eol


(* File layout *)
let version = [ at . key "version" . colon . store /[0-9.]+/ . eol ]
let include = [ at . key "include" . Util.del_ws_spc . Quote.double . eol ]
let options = [ key "options" . lbracket . [  indent . key id . indent . store Rx.no_spaces . semi . eol ]* . rbracket . eol]

(* Define lens | options | statement | log *)
let lns = ( version | include | options | empty | comment )

let filter = incl "/etc/syslog-ng.conf"
                . Util.stdexcl

let xfm = transform lns filter
