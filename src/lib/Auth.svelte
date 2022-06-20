<script>
    import {supabase} from "$lib/supabaseClient"

    let loading = false
    let email;

    const handleLogin = async () => {
        console.log("Here")
        try {
            loading = true
            const { error } = await supabase.auth.signIn({ email })
            if (error) throw error
            alert('Check your email for the login link!')
        } catch (error) {
            alert(error.error_description || error.message)
        } finally {
            loading = false
        }
    }
</script>

<div class="row backgroundimg g-0">
    <div class="container d-flex align-items-center">
        <div class="container">
            <div class="row g-0">
                <div class="col display-1 text-white text-center">Welcome to Human Flourishing</div>
            </div>
            <div class="row g-0">
                <div class="col text-white text-center p-5">
                    HF makes the work a better place by helping you do the things that make you happiest.
                </div>
            </div>
            <div class="row g-0 p-3">
                <div class="d-flex justify-content-center">
                    <form class="row row-cols-lg-auto g-3 align-items-center" on:submit|preventDefault={handleLogin}>
                        <div class="col-12">
                            <input
                                    class="inputField form-control"
                                    type="email"
                                    placeholder="Your email"
                                    bind:value={email}
                            />
                        </div>
                        <div class="col-12 text-center">
                            <input type="submit" class='btn btn-primary btn-' value={loading ? "Loading" : "Sign in/up"} disabled={loading} />
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .backgroundimg {
        background-image: url("/lighthouse.jpg");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        height: 100vh;
        width: 100%
    }
</style>