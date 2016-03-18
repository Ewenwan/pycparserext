from __future__ import print_function
import pytest


def test_asm_volatile_1():
    src = """
    void read_tsc(void) {
        long val;
        asm("rdtsc" : "=A" (val));
    }    """
    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))


def test_asm_volatile_2():
    src = """
    void read_tsc(void) {
        long val;
        asm volatile("rdtsc" : "=A" (val));
    }    """
    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))


def test_asm_volatile_3():
    src = """
    void read_tsc(void) {
        long fpenv;
        asm("mtfsf 255,%0" :: "f" (fpenv));
    }    """
    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))


def test_funky_header_code():
    src = """
        extern __inline int __attribute__ ((__nothrow__)) __signbitf (float __x)
         {
           int __m;
           __asm ("pmovmskb %1, %0" : "=r" (__m) : "x" (__x));
           return __m & 0x8;
         }
        """

    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))


@pytest.mark.parametrize("typename", ["int", "uint"])
def test_opencl(typename):
    from pycparserext.ext_c_parser import OpenCLCParser
    src = """
            __kernel void zeroMatrix(__global float *A, int n,  __global float * B)
            {
                %s i = get_global_id(0);
                for (int k=0; k<n; k++)
                    A[i*n+k] = 0;
            }
            """ % typename

    p = OpenCLCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import OpenCLCGenerator
    print(OpenCLCGenerator().visit(ast))


def test_array_attributes():
    src = """
        int x[10] __attribute__((unused));
        int y[20] __attribute((aligned(10)));
        """

    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))


def test_func_decl_attribute():
    src = """
    extern void int happy(void) __attribute__((unused));
    int main()
    {
    }
    """

    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))

def test_func_ret_ptr_decl_attribute():
    src = """
    extern void* memcpy(const void* src, const void *dst, int len) __attribute__((unused));
    """
    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))

def test_array_ptr_decl_attribute():
    src = """
    int* __attribute__((weak)) array[256];
    """
    from pycparserext.ext_c_parser import GnuCParser
    p = GnuCParser()
    ast = p.parse(src)
    ast.show()

    from pycparserext.ext_c_generator import GnuCGenerator
    print(GnuCGenerator().visit(ast))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        from py.test.cmdline import main
        main([__file__])
