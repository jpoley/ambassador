# Access Control
---
Ambassador Pro authentication is managed with the `Policy` custom resource definition (CRD). This resource allows you to specify which routes should and should not be authenticated by the authentication service. By default, all routes require authentication from the IDP with either a JWT or via a login service. 

## Authentication Policy 
A `rule` for the `Policy` CRD is a set of hosts, paths, and permission settings that indicate which routes require authentication from Ambassador Pro as well as the access rights that particular API needs. The default rule is to require authentication from all paths on all hosts. 

### Rule Configuration Values
| Value     | Example    | Description |
| -----     | -------    | -----------                  |
| `host`    | "*", "foo.com" | the Host that a given rule should match |
| `path`    | "/foo/url/"    | the URL path that a given rule should match to |
| `public`  | true           | a boolean that indicates whether or not authentication is required; default false |
| `scopes`  | openid | the rights that need to be granted in a given API. Not all APIs will need a scope defined.<br> e.g. `scope: openid` is required for OIDC conformant authentication servers |

### Examples
The following policy is shown in the [OAuth/OIDC Authentication](/user-guide/oauth-oidc-auth#test-the-auth0-application) guide and is used to secure the example `httpbin` service. 

```
apiVersion: getambassador.io/v1beta1
kind: Policy
metadata:
  name: httpbin-policy
spec:
  rules:
  - host: "*"
    path: /httpbin/ip
    public: true
    scope: openid
  - host: "*"
    path: /httpbin/user-agent/*
    public: false
    scope: openid
  - host: "*"
    path: /httpbin/headers/*
    scope: openid
```
The `Policy` defines rules based on matching the `host` and `path` to a request and refers to the `public` attribute to decide whether or not it needs to be authenticated. Since both `host` and `path` support wildcards, it is easy to configure an entire mapping to need to be authenticated or not. 

```
apiVersion: getambassador.io/v1beta1
kind: Policy
metadata:
  name: mappings-policy
spec:
  rules:
  - host: "*"
    path: /httpbin/*
    public: true
  - host:
    path: /qotm/*
    public: false
  - host: "*"
    path: /*
    public: false
```
The above `policy` configures Ambassador Pro authentication to

1. Not require authentication for the `httpbin` mapping.
2. Require authentication for the `qotm` mapping.
3. Explicitly express the default requiring authentication for all routes. 

#### Mutliple Domains

```
apiVersion: getambassador.io/v1beta1
kind: Policy
metadata:
  name: multi-domain-policy
spec:
  rules:
  - host: foo.bar.com
    path: /qotm/
    public: true
  - host: example.com
    path: /qotm/
    public: false
```
Imagine you have multiple domains behind Ambassador Pro. A domain `foo.bar.com` and `example.com`. Imagine a service named `qotm` sits behind both of these domains, you want `foo.bar.com` to have public access to `qotm` without authenticating but requests from `example.com` require authentication. The above mapping will accomplish this. 

#### Pass-Through by Default
```
---
apiVersion: getambassador.io/v1beta1
kind: Policy
metadata:
  name: default-policy
spec:
  rules:
  - host: "*"
    path: /*
    public: true
```
This policy will change the default to not require authentication for all routes. **Note** Rules applied to higher-level paths, e.g. `/qotm/`, will take precedence over ones applied to lower-level paths, e.g `/`.