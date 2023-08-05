
# Flint

*Flint* is a source-code static analyzer and quality checker for fortran programming language. It intends to follows the coding conventions mentioned [OMS Documentation Wiki page](https://alm.engr.colostate.edu/cb/wiki/16983)

Many Fortran Linter software exists, and are giants full of wisdom compared to the midget *flint*. The goal of *Flint* is to provide a Free, quickly installed, (and soon customizable) linter for Continuous Integration.


## Installation

Install Flint from Python Package index "Flinter" (because Flint was already taken =_=)


```
>pip install flinter
```

## Usage

FLint provide a CLI with the command currently implemented. 

```
>flint
  --------------------    FLINT  ---------------------

  .      - Flint, because our code stinks... -

  You are now using the Command line interface of Flint, a Fortran linter
  created at CERFACS (https://cerfacs.fr).

  This is a python package currently installed in your python environement.

Options:
  --help  Show this message and exit.

Commands:
  cplx  Score the complexity of .f90 FILE.
  fmt   Score the formatting of .f90 FILE.
```

### Formatting score

To get the score with respect to the coding convention (up to 0.2 the only convention implemented is the COlostate Univ. convention):

```
> flint fmt awesomecode.f90
5:24: Missing space after ponctuation :
 SUBROUTINE laxwe ( grid,nvert,nglen,res_c,res_spec_c,res_fic_c,snc,&
                        ^
5:30: Missing space after ponctuation :
 SUBROUTINE laxwe ( grid,nvert,nglen,res_c,res_spec_c,res_fic_c,snc,&
                              ^
(...)
329:116: Missing space after ponctuation :
             dw_fic_c_nv(k,nv,n) = dw_fic_c_nv(k,nv,n) - scale0 * ( ajrc*snc(1,nv,n) + bjrc*snc(2,nv,n) + cjrc*snc(3,nv,n) )
                                                                                                                    ^
329:119: Missing space after ponctuation :
             dw_fic_c_nv(k,nv,n) = dw_fic_c_nv(k,nv,n) - scale0 * ( ajrc*snc(1,nv,n) + bjrc*snc(2,nv,n) + cjrc*snc(3,nv,n) )
                                                                                                                       ^
--------------------------------------------------
Your code has been rated 0.56/10



Missing space after ponctuation 99
Types should be lowercased 29
Missing spaces around operator 4
Missing space before operator 4
Missing space after operator 4
Missing spaces around "=" 20

```

### Structure score

This score is against several rules taken from pep008 ensuring readability and maintanability.

```
>flint cplx awesomecode.f90

SUBROUTINE laxwe ( grid,nvert,nglen,res_c,res_spec_c,res_fic_c,snc,&

SUBROUTINE laxwe ( grid,nvert,nglen,res_c,res_spec_c,res_fic_c,snc,&
laxwe :
   too-many-lines : 270/50
   line-too-long : 106/100
   line-too-long : 106/100
   line-too-long : 106/100
   line-too-long : 106/100
   line-too-long : 106/100
   line-too-long : 113/100
   line-too-long : 111/100
   too-many-locals : 92/12
   invalid-name : local var u is too short
   invalid-name : local var v is too short
   invalid-name : local var ww is too short
   invalid-name : local var H is too short
   invalid-name : local var dP is too short
   invalid-name : local var n is too short
   invalid-name : local var nv is too short
   invalid-name : local var k is too short
   too-many-arguments : 8/5
   invalid-name : argument  is too short

------------------------------------------------------------------
Your code has been rated at 2.96/10

```


# Limitations

*Flint* is working only in the scope of a single file. Next versions will handle full project arborecence.

Moreover, a single convention is provided for now. Next versions will allow customisable conventions (err.. to a certain extent, of course)

# Acknowledgement

Flint is a service created in the [EXCELLERAT Center Of Excellence](https://www.excellerat.eu/wp/), funded by the European comunity.
![logo](http://cerfacs.fr/coop/whatwedo/logo_excellerat.png)