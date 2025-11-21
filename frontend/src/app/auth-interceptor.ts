import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {

  // Evitar error SSR: solo ejecutar en navegador
  if (typeof window === 'undefined') {
    return next(req);
  }

  const token = localStorage.getItem('token');

  // Si no hay token, no modificamos nada
  if (!token) {
    return next(req);
  }

  // Clonamos la request agregando la cabecera Authorization
  const authReq = req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });

  return next(authReq);
};
