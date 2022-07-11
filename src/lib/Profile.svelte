<script>
  import { supabase } from '$lib/supabaseClient'
  import { user } from '$lib/sessionStore'

  let loading = true
  let username = null
  let website = null
  let avatar_url = null
  let points = null

  async function getActivities() {
    try {
      const user = supabase.auth.user()
      loading = true
      let { data, error, status } = await supabase
              .from('activities')
              .select("*")
              .eq('user_id', user.id)

      if (error && status !== 406) throw error

      if (data) {
        console.log(data)
        return data
      }
    } catch (error) {
      alert(error.message)
    } finally {
      loading = false
    }
  }
  let myActivities = getActivities()

  async function getEvents() {
    try {
      const user = supabase.auth.user()
      loading = true
      let { data, error, status } = await supabase
              .from('events')
              .select('*')
              .eq('organizer_id', user.id)

      if (error && status !== 406) throw error

      if (data) {
        return data
      }
    } catch (error) {
      alert(error.message)
    } finally {
      loading = false
    }
  }
  let myEvents = getEvents()

  async function getProfile() {
    try {
      loading = true
      const user = supabase.auth.user()

      let { data, error, status } = await supabase
              .from('profiles')
              .select(`username, website, avatar_url, points`)
              .eq('id', user.id)
              .single()

      if (error && status !== 406) throw error

      if (data) {
        username = data.username
        website = data.website
        avatar_url = data.avatar_url
        points = data.points
      }
    } catch (error) {
      alert(error.message)
    } finally {
      loading = false
    }
  }

  async function updateProfile() {
    try {
      loading = true
      const user = supabase.auth.user()

      const updates = {
        id: user.id,
        username,
        website,
        avatar_url,
        updated_at: new Date(),
      }

      let { error } = await supabase.from('profiles').upsert(updates, {
        returning: 'minimal', // Don't return the value after inserting
      })

      if (error) throw error
    } catch (error) {
      alert(error.message)
    } finally {
      loading = false
    }
  }

  async function signOut() {
    try {
      loading = true
      let { error } = await supabase.auth.signOut()
      if (error) throw error
    } catch (error) {
      alert(error.message)
    } finally {
      loading = false
    }

  }

</script>

<div class="container">
  <div class="display-3 pb-5">Human Flourishing</div>
  <div class="row">
    <div class="col-md m-3 d-flex align-items-center justify-content-center">
      <div class="display-1 text-center">
        {#if points !== null}
          {points}
        {:else}
          <i class="fa fa-spinner fa-pulse fa-fw" aria-hidden="true"/>
        {/if}
      </div>
    </div>

    <div class="col">
      <form use:getProfile on:submit|preventDefault={updateProfile}>
        <div class="row mb-3 mt-5">
          <label for="email" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input id="email" type="text" class="form-control" value={$user.email} disabled />
          </div>
        </div>
        <div class="row mb-3">
          <label for="username" class="col-sm-2 col-form-label">Name</label>
          <div class="col-sm-10">
            <input
                    id="username"
                    type="text"
                    bind:value={username}
                    class="form-control"
            />
          </div>
        </div>
        <div class="row mb-3">
          <label for="website" class="col-sm-2 col-form-label">Website</label>
          <div class="col-sm-10">
            <input
                    id="website"
                    type="website"
                    bind:value={website}
                    class="form-control"
            />
          </div>
        </div>

        <div class="d-flex justify-content-between">

          <div>
            <input type="submit" class="btn btn-primary" value={loading ? 'Loading ...' : 'Update'} disabled={loading}/>
          </div>

          <div>
            <button class="btn btn-outline-primary my-5" on:click={signOut} disabled={loading}>
              Sign Out
            </button>
          </div>
        </div>
      </form>
    </div>

  </div>

  <a href="/users/{username}/{supabase.auth.user().id}" class="btn btn-primary">Show your QR Code to attend an event</a>

  <p class="mt-5">Click here to start an event. An event is any gathering of 2 or more people.</p>
  <a href="/events" class="btn btn-primary btn-lg">Start an event</a>

  <h2 class="mt-5">Activities</h2>
  {#await myActivities}
    <i class="fa fa-spinner fa-pulse fa-fw" aria-hidden="true"/>
  {:then activities}
    {#if activities}
      <table class="table">
        <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Name</th>
          <th scope="col">Points</th>
        </tr>
        </thead>
        <tbody>

        {#each activities as activity}
          <tr>
            <td>{activity.created_at}</td>
            <td>{activity.kind}</td>
            <td>{activity.points}</td>
          </tr>
        {/each}
        </tbody>
      </table>
    {:else}
      <h3>No activities. Why not attend an event?</h3>
    {/if}
  {/await}

  <h2 class="mt-5">Your previous events:</h2>
  {#await myEvents}
    <i class="fa fa-spinner fa-pulse fa-fw" aria-hidden="true"/>
  {:then events}
    {#if events}
      <table class="table">
        <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Name</th>
        </tr>
        </thead>
        <tbody>
        {#each events as event}
          <tr>
            <td><a href="/events/{event.id}">{event.created_at}</a></td>
            <td>{event.name}</td>
          </tr>
        {/each}
        </tbody>
      </table>
    {:else}
      <h3>No events. Why not start one above?</h3>
    {/if}
  {/await}
</div>
