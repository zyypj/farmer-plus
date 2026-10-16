package com.zyypj.farmerplus.platform;

import java.util.ServiceLoader;

public final class Services {

    public static final RegistrationPlatform REGISTRATION = load(RegistrationPlatform.class);

    private Services() {
    }

    private static <T> T load(Class<T> type) {
        return ServiceLoader.load(type, Services.class.getClassLoader())
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("No platform implementation found for " + type.getName()));
    }
}
