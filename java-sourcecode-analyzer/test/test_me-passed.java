
import java.lang.reflect.Method;
import java.util.Set;

import net.sf.cglib.beans.BeanMap;
import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodProxy;
import net.sf.cglib.proxy.MethodInterceptor;

public class TestMyClass {
	
	
	
	public static void main(String[] argv){
		
		try{ //
			throw new MyExceptionClassSecond("abc");
		}catch(Exception ex){
			System.out.println(ex.getMessage());
		}
	}
	/**
	 * 
	 * @param args
	 */
/*
	 * 
*/
	public static void main1(String[] args)
	{
        Enhancer e = new Enhancer();
        //e.setSuperclass(clazz);
        //e.setCallback(callback);
        Class[] argumentTypes =  new Class[1];
        argumentTypes[0] = String.class;
        String arguments[] =new String[1];
        arguments[1]="def";
        e.create(argumentTypes, arguments);
	}

	public static void main2(String[] args) {

		Enhancer enhancer = new Enhancer();

		enhancer.setSuperclass(CloudStackException.class);
		enhancer.setCallback(new MethodInterceptorImpl());

		CloudStackException my = (CloudStackException) enhancer.create();
		boolean interceptDuringConstruction=true;
		enhancer.setInterceptDuringConstruction(interceptDuringConstruction);
		

		my.method();
		
		
		 
			try {
				//MyExceptionClassSecond abc =new  MyExceptionClassSecond("abc");
				MyExceptionClassSecond abc = CreateExceptionInstance.create("MyExceptionClassSecond","abc");
				throw   abc;
			} catch (MyExceptionClassSecond e) {
				System.out.println( e.getMessage() );
			}
		 
		
		CloudStackException mytrue = new CloudStackException();
		
		Set keyset = BeanMap.create(  mytrue ).keySet();
		 
			BeanMap map = BeanMap.create(mytrue);
			for (Object key : keyset) {
				map.get(key);
			}

		 
		
	}

	private static class MethodInterceptorImpl implements MethodInterceptor {

		
		public Object intercept(Object obj, Method method, Object[] args,
				MethodProxy proxy) throws Throwable {

			System.out.println(method);

			
			proxy.invokeSuper(obj, args);

			return null;
		}
	}
}