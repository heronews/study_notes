# cmake
## install
### GET_RUNTIME_DEPENDENCIES
```
if(MSVC)
    install(CODE "
        file(GET_RUNTIME_DEPENDENCIES
        EXECUTABLES $<TARGET_FILE:SoyMap>
        RESOLVED_DEPENDENCIES_VAR resolved_deps
        UNRESOLVED_DEPENDENCIES_VAR unresolved_deps
        DIRECTORIES ${CMAKE_PREFIX_PATH}/bin
        POST_EXCLUDE_REGEXES \"system32\")

        message(STATUS \"resolved deps:\")
        foreach(dep \${resolved_deps})
            message(STATUS \" - \${dep}\")
        endforeach()
        file(INSTALL DESTINATION \"${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}\" TYPE SHARED_LIBRARY FILES \${resolved_deps})

        message(STATUS \"unresolved deps:\")
        foreach(dep \${unresolved_deps})
            message(STATUS \" - \${dep}\")
        endforeach()
    ")
endif()
```