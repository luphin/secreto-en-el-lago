"use client";

import { Input, IconButton, InputGroup } from "@chakra-ui/react";
import { forwardRef, useState } from "react";
import { LuEye, LuEyeOff } from "react-icons/lu";

export interface PasswordInputProps extends React.ComponentPropsWithoutRef<typeof Input> {
    placeholder?: string;
}

export const PasswordInput = forwardRef<HTMLInputElement, PasswordInputProps>(
    function PasswordInput(props, ref) {
        const [show, setShow] = useState(false);
        const handleClick = () => setShow(!show);

        return (
            <InputGroup endElement={
                <IconButton
                    variant="ghost"
                    aria-label={show ? "Ocultar contraseña" : "Mostrar contraseña"}
                    onClick={handleClick}
                    size="sm"
                    tabIndex={-1}
                >
                    {show ? <LuEyeOff /> : <LuEye />}
                </IconButton>
            }>
                <Input
                    ref={ref}
                    type={show ? "text" : "password"}
                    {...props}
                />
            </InputGroup>
        );
    }
);
