"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Box, Spinner } from "@chakra-ui/react";
import AuthService from "@/services/auth.service";

export default function UserLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    const token = AuthService.getToken();

    if (!token) {
      // No hay token, redirigir a login
      router.push("/login");
    } else {
      // Hay token, permitir acceso
      setIsChecking(false);
    }
  }, [router]);

  // Mostrar spinner mientras verifica autenticación
  if (isChecking) {
    return (
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        minH="100vh"
        bg="bg.canvas"
      >
        <Spinner size="xl" color="purple.500" />
      </Box>
    );
  }

  return <>{children}</>;
}
