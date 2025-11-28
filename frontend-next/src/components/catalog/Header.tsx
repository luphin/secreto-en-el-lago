"use client";

import { Flex, Heading, Button, Group, Input, InputGroup} from "@chakra-ui/react";
import { LuSearch, LuUser, LuBookOpen } from "react-icons/lu";
import NextLink from "next/link";
import { useAuth } from "@/contexts/AuthContext";

export function Header() {
  const { isAuthenticated } = useAuth();

  return (
    <Flex
      as="header"
      p={6}
      borderBottomWidth="1px"
      bg="bg.panel"
      gap={4}
      direction={{ base: "column", md: "row" }}
      align={{ base: "stretch", md: "center" }}
      justify="space-between"
    >
			<NextLink href="/">
				<Heading size="lg" color="blue.600" _hover={{ color: "blue.700" }} transition="color 0.2s">
					Biblioteca Digital
				</Heading>
			</NextLink>

			<InputGroup flex="1" maxW={{ base: "full", md: "700px"}} startElement={<LuSearch />}>
				<Input placeholder="Buscar libros, autores, categorías..." size="md"/>
			</InputGroup>

      <Group gap={3}>
        {isAuthenticated ? (
          <Button
            asChild
            colorPalette="blue"
            size="md"
          >
            <NextLink href="/dashboard">
              <LuBookOpen />
              Mis Libros
            </NextLink>
          </Button>
        ) : (
          <Button
            asChild
            variant="outline"
            colorPalette="blue"
            size="md"
          >
            <NextLink href="/login">
              <LuUser />
              Iniciar sesión
            </NextLink>
          </Button>
        )}
      </Group>
    </Flex>
  );
}
