"use client";

import { Group, Box, type GroupProps } from "@chakra-ui/react";
import { cloneElement, forwardRef, type ReactNode } from "react";

export interface InputGroupProps {
  startElement?: React.ReactElement;
  endElement?: React.ReactElement;
  children?: ReactNode;
  flex?: string;
  maxW?: Record<string, string> | string;
  [key: string]: any;
}

export const InputGroup = forwardRef<HTMLDivElement, InputGroupProps>(
  function InputGroup(props, ref) {
    const {
      startElement,
      endElement,
      children,
      ...rest
    } = props;

    return (
      <Group ref={ref} attached {...rest}>
        {startElement && (
          <Box
            display="flex"
            alignItems="center"
            px={3}
            borderWidth="1px"
            borderRightWidth="0"
            borderRadius="md"
            borderTopRightRadius="0"
            borderBottomRightRadius="0"
            bg="bg.muted"
            color="gray.500"
          >
            {cloneElement(startElement)}
          </Box>
        )}
        {children}
        {endElement && (
          <Box
            display="flex"
            alignItems="center"
            px={3}
            borderWidth="1px"
            borderLeftWidth="0"
            borderRadius="md"
            borderTopLeftRadius="0"
            borderBottomLeftRadius="0"
            bg="bg.muted"
            color="gray.500"
          >
            {cloneElement(endElement)}
          </Box>
        )}
      </Group>
    );
  }
);
